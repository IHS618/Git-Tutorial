#!/usr/bin/env python
import numpy as np
from make_latex import ExportTopologyToLatex

np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)

# constants ====================================================================
LOW_SNR = np.float32(-999)
LARGE_CW = 2048
MAX_CW = 1024
MIN_CW = 16
REFERENCE_LOSS = 46.6777  
REFERENCE_DIST = 1 
EXPONENT_MODEL = 3  
EXPONENT_REAL = 2.5
REFERENCE_TX_POWER = 20  
NOISE_FLOOR = -93.97 
SNR_THRESHOLD = 23
DEFAULT_CS_THRESHOLD = -82
TIMESLOTS_PER_TX = 32
SINGLE_CH_TPUT = 30.0
# ===============================================================================

# utility functions ============================================================


def DB2W(p_db):  
    return np.power(10, p_db/10)


def W2DB(p):  
    return 10 * np.log10(p)


def GetDist(a, b):  
    return np.sqrt(np.square(a[0]-b[0]) + np.square(a[1]-b[1]))


def GetPathLossDB(distance):  
    if(distance <= REFERENCE_DIST):
        return REFERENCE_LOSS
    else:
        return REFERENCE_LOSS + 10*EXPONENT_REAL*np.log10(distance/REFERENCE_DIST)


def GetPathLossDB_Model(distance):  
    if(distance <= REFERENCE_DIST):
        return REFERENCE_LOSS
    else:
        return REFERENCE_LOSS + 10*EXPONENT_MODEL*np.log10(distance/REFERENCE_DIST)


def GetRxPowerDB(a, b):   
    return REFERENCE_TX_POWER - GetPathLossDB(GetDist(a, b))


def GetRxPowerDB_Model(a, b):  
    return REFERENCE_TX_POWER - GetPathLossDB_Model(GetDist(a, b))


def GetDistFromPL(pl):  
    if pl <= REFERENCE_LOSS:
        return REFERENCE_DIST
    dist = np.power(10, (pl - REFERENCE_LOSS) /
                    (10 * EXPONENT_MODEL)) * REFERENCE_DIST
    return dist


def GetMinCSThresh(dist_to_ap):
    rx_power = REFERENCE_TX_POWER - GetPathLossDB_Model(dist_to_ap)
    ni_power = rx_power - SNR_THRESHOLD
    ni_pl = REFERENCE_TX_POWER - ni_power
    ni_dist = GetDistFromPL(ni_pl)
    max_pl = GetPathLossDB_Model(dist_to_ap + ni_dist)
    min_cs = REFERENCE_TX_POWER - max_pl
    return min_cs


def GetNearestAP(ms, aps):
    min_dist_ap = 0
    min_dist = GetDist(ms, aps[0])
    for i in range(1, aps.shape[0]):
        dist = GetDist(ms, aps[i])
        if dist < min_dist:
            min_dist = dist
            min_dist_ap = i
    return min_dist_ap
# ===============================================================================

# Operation functions ==========================================================


def CarrierSenseAP(ap_ind, tx_vector, aps, threshold=DEFAULT_CS_THRESHOLD):  
    if tx_vector[ap_ind] == 1:
        return True
    total_interference_w = 0.0
    for i in range(len(aps)):
        if tx_vector[i] == 1:
            total_interference_w += DB2W(GetRxPowerDB(aps[i], aps[ap_ind]))
    if total_interference_w == 0.0:
        return False
    total_interference_db = W2DB(total_interference_w)
    if(total_interference_db > threshold):
        return True  # busy
    else:
        return False  # idle

# -------------------------------------------------------------------------------


def DSCCarrierSenseAP(ap_ind, tx_vector, tx_dest, aps, mss, MARGIN=0):
    if tx_vector[ap_ind] == 1:
        return True

    # calculate my CST
    req_cst = GetMinCSThresh(
        GetDist(aps[ap_ind], mss[tx_dest[ap_ind]])) - MARGIN
    total_interference_w = 0.0

    for i in range(len(aps)):
        if tx_vector[i] == 1:
            total_interference_w += DB2W(GetRxPowerDB(aps[i], aps[ap_ind]))
    if total_interference_w == 0.0:
        return False
    total_interference_db = W2DB(total_interference_w)
    if total_interference_db > req_cst:
        return True
    else:
        return False

# -------------------------------------------------------------------------------


def SmartCarrierSenseAP(ap_ind, tx_vector, tx_dest, aps, mss, MARGIN=0):
    if tx_vector[ap_ind] == 1:
        return True

    # for each interfering node, see if both transmissions could be safe ---------
    total_interference_w = 0.0
    req_cst = GetMinCSThresh(
        GetDist(aps[ap_ind], mss[tx_dest[ap_ind]])) - MARGIN
    for i in range(len(aps)):
        if i == ap_ind:
            continue
        if tx_vector[i] == 1:
            ilevel = GetRxPowerDB(aps[i], aps[ap_ind])
            if ilevel > GetMinCSThresh(GetDist(aps[i], mss[tx_dest[i]])) - MARGIN:
                return True
            else:
                total_interference_w += DB2W(ilevel)
            if ilevel > req_cst:
                return True
    total_interference_db = W2DB(total_interference_w)
    if total_interference_db > req_cst:
        return True
    else:
        return False

# -------------------------------------------------------------------------------


def NewCarrierSenseAP(ap_ind, tx_vector, tx_dest, aps, mss, MARGIN=0):
    # if I am already a transmitter, I do not need carrier sensing.
    if tx_vector[ap_ind] == 1:
        return True

    # If I transmit, can my receiver successfully receive the packet?
    for i in range(len(aps)):
        if i == ap_ind:
            continue
        if tx_vector[i] == 1:
            ilevel = GetRxPowerDB(aps[i], mss[tx_dest[ap_ind]])
            slevel = GetRxPowerDB(aps[ap_ind], mss[tx_dest[ap_ind]])
            if slevel - ilevel < SNR_THRESHOLD + MARGIN:
                return True

    # If I transmit, will my transmission destroy the on-going transmission?
    for i in range(len(aps)):
        if i == ap_ind:
            continue
        if tx_vector[i] == 1:
            ilevel = GetRxPowerDB(aps[ap_ind], mss[tx_dest[i]])
            slevel = GetRxPowerDB(aps[i], mss[tx_dest[i]])
            if slevel - ilevel < SNR_THRESHOLD + MARGIN:
                return True

    return False
# -------------------------------------------------------------------------------


# TransmitAP: AP transmits to MS -----------------------------------------------
def TransmitAP(tx_vector, tx_dest, mss, aps):
    rx_vector = np.copy(tx_vector)
    rx_snr = np.zeros(tx_vector.shape)
    for i in range(len(aps)):
        if tx_vector[i] == 1:
            # AP i is transmitting to tx_dest[i]
            signal_db = GetRxPowerDB(aps[i], mss[tx_dest[i]])
            total_noise_w = DB2W(NOISE_FLOOR)
            # calculate interference
            for j in range(len(aps)):
                if i == j or tx_vector[j] == 0:
                    continue
                total_noise_w += DB2W(GetRxPowerDB(aps[j], mss[tx_dest[i]]))
            total_noise_db = W2DB(total_noise_w)
            snr_db = signal_db - total_noise_db
            rx_snr[i] = snr_db
            if(snr_db < SNR_THRESHOLD):
                rx_vector[i] = 0
        else:
            rx_snr[i] = LOW_SNR
    return rx_vector, rx_snr
# ===============================================================================


NUM_GRID=3 
SEED=1000
NUM_NODES=0
NODES_PER_CELL=1
AREA_SIZE=10
#NUM_CH=1
NUM_CH=4
CS=-82
END=1000
VERBOSE=True
CH_BW_LOSS=0.04
LATEX=False
#IDEAL=False
IDEAL=True
MARGIN=0.0
TOKEN=False
PROTO=0

# Simulation Setup ===========================================================

# set parameters -------------------------------------------------------------
param_seed = SEED
param_num_grid = NUM_GRID
param_num_nodes_per_cell = NODES_PER_CELL
param_area_size = AREA_SIZE
param_num_aps = param_num_grid*param_num_grid

if NUM_NODES == 0:
    param_num_nodes = param_num_aps*param_num_nodes_per_cell
else:
    param_num_nodes = NUM_NODES

param_num_channels = NUM_CH
param_end_time = END
param_cs_thresh = CS
param_protocol = PROTO
param_verbose = VERBOSE
param_ch_bw_loss = CH_BW_LOSS
param_export_latex = LATEX
param_ideal = IDEAL
param_margin = MARGIN
param_token = TOKEN

# set random number generator seed -------------------------------------------
np.random.seed(param_seed)

# declare APs and mobile stations --------------------------------------------
aps = np.zeros((param_num_aps, 2))                                    # x, y
print("aps \n", aps)
mss = np.zeros((param_num_nodes, 2))                                  # x, y
print("mss \n", mss)
asc = np.zeros((param_num_nodes)).astype(np.int)				      # ms-ap
print("asc \n", asc)
mem = np.zeros((param_num_aps, param_num_nodes)).astype(np.int)       # connect
print("mem \n", mem)
dst = np.zeros((param_num_aps, param_num_channels)).astype(np.int)
print("dst \n", dst)
dst[:, :] = -1
print("new dst \n", dst)
chs = np.zeros((param_num_nodes, param_num_channels)).astype(np.int)  # channel
print("chs \n", chs)
cws = np.zeros((param_num_aps, param_num_channels)).astype(np.int)    # contention window
print("cws \n", cws)
mcw = np.zeros((param_num_aps, param_num_channels)).astype(np.int)    # maximum contention window
print("mcw \n", mcw)
cst = np.zeros((param_num_channels))
print("cst \n", cst)

print("=============================================")
print("=============================================")
#=============================================================================
# deploy APs -----------------------------------------------------------------
for i in range(param_num_grid):
    for j in range(param_num_grid):
        aps[i*param_num_grid+j,
            0:2] = np.array([j, i]) * param_area_size + param_area_size/2
print("deploy APs : aps \n", aps)

# deploy mobile stations -----------------------------------------------------
if NUM_NODES == 0:
    for i in range(param_num_aps):
        for j in range(param_num_nodes_per_cell):
            base = (np.random.rand(2)*2-1)*param_area_size/2
            ind = i * param_num_nodes_per_cell + j
            mss[ind, 0:2] = aps[i] + base
else:
    # random deployment --------------------------------------------------------
    for i in range(param_num_nodes):
        mss[i, 0:2] = np.random.rand(2) * param_area_size * param_num_grid       
print("deploy ms : mss \n", mss)

# MANUAL (temporary) ---------------------------
#mss[0] = np.array([6,5])
#mss[1] = np.array([14,5])

# output topology to latex ---------------------------------------------------
if param_export_latex == True:
    ExportTopologyToLatex(param_num_grid, param_area_size, aps, mss)

# associate mobile stations with aps -----------------------------------------
for i in range(param_num_nodes):
    asc[i] = GetNearestAP(mss[i], aps)
    mem[asc[i], i] = 1  
print("associate mss with aips")
print("asc \n", asc)
print("mem \n", mem)


# set initial CW and max CW --------------------------------------------------
for i in range(param_num_aps):
    for j in range(param_num_channels):
        mcw[i, j] = MIN_CW
        cws[i, j] = np.random.randint(mcw[i, j])
print("mcw \n", mcw)
print("cws \n", cws)

# set initial carrier sense threshold ----------------------------------------
for i in range(param_num_channels):
    cst[i] = param_cs_thresh
print("cst \n", cst)

#++++++++++++++adding+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
for i in range(param_num_channels):
    cst[i] = param_cs_thresh
print("cst \n", cst)
#++++++++++++++adding+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# set channels ---------------------------------------------------------------
if param_protocol >= 0:
    for i in range(param_num_nodes):
        ch = i % param_num_channels
        chs[i, ch] = 1
print("set channels")
print("ch \n", ch)
print("chs \n", chs)        
    
# select initial destination -------------------------------------------------
for c in range(param_num_channels):
    for i in range(param_num_aps):
        for j in range(param_num_nodes):
            if mem[i, j] == 1 and chs[j, c] == 1: #ap&nd and ch&nd
                dst[i, c] = j  #node
                break
print("destination")
print("mem \n", mem)  
print("chs \n", chs) 
print("new dst 다 -1로 초기화 되어있음")         
print("dst \n", dst)


# display simulation configuration -------------------------------------------
if param_verbose == True:
    print('----------------------------------')
    print(' simulation area     : %dx%d' %
          (param_num_grid, param_num_grid))
    if NUM_NODES == 0:
        print(' nodes per cell      : %d' % param_num_nodes_per_cell)
    else:
        print(' number of nodes     : %d' % param_num_nodes)
    print(' cell size           : %.1f' % param_area_size)
    print(' number of channels  : %d' % param_num_channels)
    print(' CS threshold        : %.1f' % param_cs_thresh)
    print(' protocol            : %d' % param_protocol)
    print(' CST margin          : %d' % param_margin)
    print(' seed number         : %d' % param_seed)
    print(' end time            : %d' % param_end_time)
    if param_ideal == True:
        print(' ideal               : YES')
    else:
        print(' ideal               : NO')
    print('----------------------------------')


# Simulation Start ===========================================================
# print("=====Simulation Start=====")
# print("=====Simulation Start=====")
stat_tx_packets_ms = np.zeros(len(mss))
# print("stat_tx_packets_ms \n", stat_tx_packets_ms)
stat_tx_packets_ap = np.zeros(len(aps))
# print("stat_tx_packets_ap \n", stat_tx_packets_ap)
stat_rx_packets_ms = np.zeros(len(mss))
# print("stat_rx_packets_ms \n", stat_rx_packets_ms)
stat_rx_packets_ap = np.zeros(len(aps))
# print("stat_rx_packets_ap \n", stat_rx_packets_ap)
progress = 0

for t in range(param_end_time):

    # display progress ---------------------------------------------------------
    curr_progress = np.floor(t / param_end_time * 100)
    if curr_progress > progress:
        progress = curr_progress
        #print('Progress: %3d%%' % progress, end='\r')

    # DCF operation on each channel --------------------------------------------
    for ch in range(param_num_channels):
        
        # prepare data structures ------------------------------------------------
        cw = np.copy(cws[:, ch])
        #print("cw \n", cw)
        tx_vector = np.zeros(param_num_aps)
        #print("tx_vector \n", tx_vector)
        blocked = np.zeros(param_num_aps)
        #print("blocked \n", blocked)
        
        # block all aps that do not have a destination
        for i in range(param_num_aps):
            if dst[i, ch] == -1:
                blocked[i] = 1   #dst가 -1이면 blocked 1로
        slot_count = 0
        #print(blocked)
        
        
        # repeatedly add transmitters --------------------------------------------
        found = True
        while found: #found가 true일동안
            found = False
            if np.min(blocked) > 0:  # if all nodes are blocked, finish this channel
                break   #blocked가 모두 1이면 채널 끝

            # select transmitters based on random backoff --------------------------
            win_count = np.min(cw[blocked == 0])
            #print("[blocked == 0]", [blocked == 0])
            #print("cw[blocked == 0]", cw[blocked == 0])
            #print("win_count \n", win_count)
            if slot_count + win_count > TIMESLOTS_PER_TX:
                # no more nodes can transmit in this slot ----------------------------
                # 더이상 못보내
                cw[blocked == 0] -= (TIMESLOTS_PER_TX - slot_count)
                break
            else:
                slot_count += win_count
            addi_tx = (cw == win_count).astype(np.int) * (1-blocked)
            #print(" addi_tx",  addi_tx)

            # ideal (hack) ---------------------------------------------------------
            # no collision due to colliding backoff counter ------------------------
            if param_ideal == True:
                candidates = np.nonzero(addi_tx)[0]
                #print("candidates",candidates)
                tx = candidates[np.random.randint(len(candidates))]
                #print("tx", tx)
                ty = np.zeros(addi_tx.shape)
                #print("ty", ty)
                ty[tx] = 1
                addi_tx = ty
                #print("addi_tx", addi_tx)
            # -----------------------------------------------------------------------
            
            # add new transmitters, update cw, block all transmitters --------------
            if np.sum(addi_tx) > 0:
                found = True  #===>repeatedly
            tx_vector += addi_tx
            cw[blocked == 0] -= win_count
            blocked[addi_tx == 1] = 1

            # determine nodes blocked by the transmitters --------------------------
            for i in range(param_num_aps):
                if tx_vector[i] == 1 or blocked[i] == 1:
                    continue
                if param_protocol == 0:
                    cs = CarrierSenseAP(i, tx_vector, aps, threshold=cst[ch])
                elif param_protocol == 1:
                    cs = DSCCarrierSenseAP(i, tx_vector, dst[:, ch], aps, mss, param_margin)
                elif param_protocol == 2:
                    cs = SmartCarrierSenseAP(i, tx_vector, dst[:, ch], aps, mss, param_margin)
                elif param_protocol >= 3:
                    cs = NewCarrierSenseAP(i, tx_vector, dst[:, ch], aps, mss, param_margin)
                if cs == True:
                    blocked[i] = 1    #true-> block
        #끝 repeatedly add transmitters 끝--------------------------------------------


        # transmit packets -------------------------------------------------------
        rx_vector, _ = TransmitAP(tx_vector, dst[:, ch], mss, aps)  #return rx_vector, rx_snr
        #print("rx_vector",rx_vector)
        for i in range(len(rx_vector)):
            if rx_vector[i] == 1:
                stat_rx_packets_ms[dst[i, ch]] += 1
                # print("stat_rx_packets_ms",stat_rx_packets_ms)
                # print("stat_rx_packets_ms[dst[i, ch]]",stat_rx_packets_ms[dst[i, ch]])
                stat_rx_packets_ap[i] += 1
                # print("stat_rx_packets_ap", stat_rx_packets_ap)
                # print("stat_rx_packets_ap[i]", stat_rx_packets_ap[i])
            if tx_vector[i] == 1:
                stat_tx_packets_ms[dst[i, ch]] += 1
                stat_tx_packets_ap[i] += 1

        # update cw --------------------------------------------------------------
        for i in range(param_num_aps):
            if tx_vector[i] == 1:
                if rx_vector[i] == 0:
                    mcw[i, ch] = min(mcw[i, ch]*2, MAX_CW)
                else:
                    mcw[i, ch] = MIN_CW

                cw[i] = np.random.randint(mcw[i, ch])
                #print("cw[i]", cw[i])
                #print("cw", cw)

            # update cws -----------------------------------------------------------
            cws[i, ch] = cw[i]
            # print("cws[i, ch]", cws[i, ch])
            # print("cws", cws)

        # update destination -----------------------------------------------------
        for i in range(param_num_aps):
            if tx_vector[i] == 1:
                # select next destination (round-robin)
                if param_protocol >= 0:
                    start = dst[i, ch]
                    curr = (start + 1) % param_num_nodes
                    while curr != start:
                        if chs[curr, ch] == 1 and mem[i, curr] == 1:
                            dst[i, ch] = curr
                            break
                        else:
                            curr = (curr + 1) % param_num_nodes

# Simulation End =============================================================
#print('Simulation Complete.')
#print('ms statistics')
# print(stat_tx_packets_ms)
# print(stat_rx_packets_ms)

#print('ap statistics')
# print(stat_tx_packets_ap)
# print(stat_rx_packets_ap)
#print(' ')

total_tx = np.sum(stat_tx_packets_ms)
total_rx = np.sum(stat_rx_packets_ms)
print('number of TX packets  : %6d' % total_tx)
print('number of RX packets  : %6d' % total_rx)
print('number of lost packets: %6d' % (total_tx-total_rx))

# collect statistics ---------------------------------------------------------
tput_ms = stat_rx_packets_ms / param_end_time * SINGLE_CH_TPUT
total_tput_ms = np.sum(tput_ms)
fairness_ms = 0
if total_tput_ms > 0:
    fairness_ms = np.square(np.sum(tput_ms)) / (tput_ms.shape[0] * np.sum(np.square(tput_ms)))
   

tput_ap = stat_rx_packets_ap / param_end_time * SINGLE_CH_TPUT
total_tput_ap = np.sum(tput_ap)
fairness_ap = 0
if total_tput_ap > 0:
    fairness_ap = np.square(np.sum(tput_ap)) / (tput_ap.shape[0] * np.sum(np.square(tput_ap)))

sorted_tput_ap = np.sort(tput_ap)
bottom_25_tput_ap = np.sum(sorted_tput_ap[0:param_num_aps//4])
bottom_50_tput_ap = np.sum(sorted_tput_ap[0:param_num_aps//2])

sorted_tput_ms = np.sort(tput_ms)
bottom_25_tput_ms = np.sum(sorted_tput_ms[0:param_num_nodes//4])
bottom_50_tput_ms = np.sum(sorted_tput_ms[0:param_num_nodes//2])

if param_verbose == True:
    print('--------------------------------')
    print('        MS statistics           ')
    print('--------------------------------')
    print(' total throughput      : %.3f' % total_tput_ms)
    print(' fairness              : %.3f' % fairness_ms)
    print(' bottom 50%% throughput : %.3f' % bottom_50_tput_ms)
    print(' bottom 25%% throughput : %.3f' % bottom_25_tput_ms)
    print(' ')

# return total_tput_ms, bottom_50_tput_ms, bottom_25_tput_ms, fairness_ms, total_tx, total_rx