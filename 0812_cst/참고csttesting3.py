#!/usr/bin/env python
import numpy as np
from make_latex_cst import ExportTopologyToLatex

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)  #Deprecation Warning x

np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)

# constants ====================================================================
LOW_SNR = np.float32(-999)
LARGE_CW = 2048
MAX_CW = 1024
MIN_CW = 16
REFERENCE_LOSS = 46.6777  
REFERENCE_DIST = 1 
EXPONENT_MODEL = 3  # 논문에서 r=3
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


#+++++++++++++++adding++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# channel 논문 함수 만들기

# 채널 CST 구하기
def CSTperChannel (Ps):
    Ds = GetDistFromPL(REFERENCE_TX_POWER - Ps)
    # print("Ds", Ds) 
    
    # Di 구하기  ------------
    Di = GetDistFromPL(REFERENCE_TX_POWER - (Ps - SNR_THRESHOLD))
    # print("Di", Di) 
    
    # Pcs 구하기 ------------ new cst(?)
    Pcs = REFERENCE_TX_POWER - GetPathLossDB(Ds + Di) # +Pm
    # print("Pcs", Pcs)
    
    return Pcs

#+++++++++++++++adding++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



def GetMinCSThresh(dist_to_ap):   #---------내일 채널별 가장 먼 거리로 이 함수를 이용해서 다시 구해보기 
    rx_power = REFERENCE_TX_POWER - GetPathLossDB_Model(dist_to_ap)
    ni_power = rx_power - SNR_THRESHOLD
    ni_pl = REFERENCE_TX_POWER - ni_power
    ni_dist = GetDistFromPL(ni_pl)
    max_pl = GetPathLossDB_Model(dist_to_ap + ni_dist)  #아이패드4
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


#+++++++++++++++adding++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# new CarrierSenseAP ------------------
def CarrierSenseAP(ap_ind, tx_vector, aps, chs, mem,dst, ch, cst0, cst1, cst2, cst3, threshold=DEFAULT_CS_THRESHOLD):  
    if tx_vector[ap_ind] == 1:
        return True
    total_interference_w = 0.0
    
    for i in range(len(aps)):
        if tx_vector[i] == 1:
            total_interference_w += DB2W(GetRxPowerDB(aps[i], aps[ap_ind]))  
            
    if total_interference_w == 0.0:
        return False
    
    total_interference_db = W2DB(total_interference_w)
    for j in range(len(chs)): #ms 수          
        if mem[i,j]==1 and chs[j,ch]==1 : #연결 #and dst[i,ch]==j:
        
            if chs[j,0]==1 and ch==0 : #ch0
                if(total_interference_db > cst0):
                    return True  # busy
                else:
                    return False  # idle
                
            elif chs[j,1]==1 and ch==1:  #채널1     
                if(total_interference_db > cst1):
                    return True  # busy
                else:
                    return False  # idle
            
            elif chs[j,2]==1 and ch==2:  #채널2    
                if(total_interference_db > cst2):
                    return True  # busy
                else:
                    return False  # idle
            
            elif chs[j,3]==1 and ch==3:  #채널3    
                if(total_interference_db > cst3):
                    return True  # busy
                else:
                    return False  # idle
            
            else:
                return ("CarrierSenseAP error")
        
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ------------------------------------------------------------



# def CarrierSenseAP(ap_ind, tx_vector, aps, threshold=DEFAULT_CS_THRESHOLD):  
#     if tx_vector[ap_ind] == 1:
#         return True
#     total_interference_w = 0.0
#     for i in range(len(aps)):
#         if tx_vector[i] == 1:
#             total_interference_w += DB2W(GetRxPowerDB(aps[i], aps[ap_ind]))
#     if total_interference_w == 0.0:
#         return False
#     total_interference_db = W2DB(total_interference_w)
#     if(total_interference_db > threshold):
#         return True  # busy
#     else:
#         return False  # idle

# -------------------------------------------------------------------------------


def DSCCarrierSenseAP(ap_ind, tx_vector, tx_dest, aps, mss, MARGIN=0):
    if tx_vector[ap_ind] == 1:
        return True

    # calculate my CST
    req_cst = GetMinCSThresh(GetDist(aps[ap_ind], mss[tx_dest[ap_ind]])) - MARGIN
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


# def SmartCarrierSenseAP(ap_ind, tx_vector, tx_dest, aps, mss, MARGIN=0):
#     if tx_vector[ap_ind] == 1:
#         return True

#     # for each interfering node, see if both transmissions could be safe ---------
#     total_interference_w = 0.0
#     req_cst = GetMinCSThresh(GetDist(aps[ap_ind], mss[tx_dest[ap_ind]])) - MARGIN
#     for i in range(len(aps)):
#         if i == ap_ind:
#             continue
#         if tx_vector[i] == 1:
#             ilevel = GetRxPowerDB(aps[i], aps[ap_ind])
#             if ilevel > GetMinCSThresh(GetDist(aps[i], mss[tx_dest[i]])) - MARGIN:
#                 return True
#             else:
#                 total_interference_w += DB2W(ilevel)
#             if ilevel > req_cst:
#                 return True
#     total_interference_db = W2DB(total_interference_w)
#     if total_interference_db > req_cst:
#         return True
#     else:
#         return False
    
    
# -----내가 다시 만드는 중 ------------------------------------
def SmartCarrierSenseAP(ap_ind, tx_vector, tx_dest, aps, mss, MARGIN=0):
    if tx_vector[ap_ind] == 1:
        return True

    # for each interfering node, see if both transmissions could be safe ---------
    total_interference_w = 0.0
    
    
    req_cst = GetMinCSThresh(GetDist(aps[ap_ind], mss[tx_dest[ap_ind]])) - MARGIN
    for i in range(len(aps)):
        if i == ap_ind:
            continue
        if tx_vector[i] == 1:
            ilevel = GetRxPowerDB(aps[i], aps[ap_ind])
            
            for j in range(len(mss)): # ms수
                if mem[i,j]==1 and chs[j,ch]==1 :
                    
                    if chs[j,0]==1 and ch==0:
                        if ilevel > GetMinCSThresh(GetDist(aps[i], mss[tx_dest[i]])) - MARGIN:
                            return True
                        else:
                            total_interference_w += DB2W(ilevel)
                        if ilevel > cst0:
                            return True
                    
                    if chs[j,1]==1 and ch==1:
                        if ilevel > GetMinCSThresh(GetDist(aps[i], mss[tx_dest[i]])) - MARGIN:
                            return True
                        else:
                            total_interference_w += DB2W(ilevel)
                        if ilevel > cst1:
                            return True
                        
                    if chs[j,2]==1 and ch==2:
                        if ilevel > GetMinCSThresh(GetDist(aps[i], mss[tx_dest[i]])) - MARGIN:
                            return True
                        else:
                            total_interference_w += DB2W(ilevel)
                        if ilevel > cst2:
                            return True
                        
                    if chs[j,3]==1 and ch==3:
                        if ilevel > GetMinCSThresh(GetDist(aps[i], mss[tx_dest[i]])) - MARGIN:
                            return True
                        else:
                            total_interference_w += DB2W(ilevel)
                        if ilevel > cst3:
                            return True
                    
                    
            
            
            
            
            # if ilevel > GetMinCSThresh(GetDist(aps[i], mss[tx_dest[i]])) - MARGIN:
            #     return True
            # else:
            #     total_interference_w += DB2W(ilevel)
            # if ilevel > req_cst:
            #     return True
    # total_interference_db = W2DB(total_interference_w)
    # if total_interference_db > req_cst:
    #     return True
    # else:
    #     return False
    
    
    total_interference_db = W2DB(total_interference_w)
    for j in range(len(mss)): #ms 수          
        if mem[i,j]==1 and chs[j,ch]==1 : #연결 #and dst[i,ch]==j:
        
            if chs[j,0]==1 and ch==0 : #ch0
                if(total_interference_db > cst0):
                    return True  # busy
                else:
                    return False  # idle
                
            elif chs[j,1]==1 and ch==1:  #채널1     
                if(total_interference_db > cst1):
                    return True  # busy
                else:
                    return False  # idle
            
            elif chs[j,2]==1 and ch==2:  #채널2    
                if(total_interference_db > cst2):
                    return True  # busy
                else:
                    return False  # idle
            
            elif chs[j,3]==1 and ch==3:  #채널3    
                if(total_interference_db > cst3):
                    return True  # busy
                else:
                    return False  # idle
            
            else:
                return ("smartCarrierSenseAP error")


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
#NUM_GRID=10
SEED=1000
#NUM_NODES=0
NUM_NODES=22
#NUM_NODES=100
NODES_PER_CELL=1
#NODES_PER_CELL=4
AREA_SIZE=10
#NUM_CH=1
NUM_CH=4
CS=-82
END=1000
VERBOSE=True
CH_BW_LOSS=0.04
LATEX=False
IDEAL=False
#IDEAL=True
#MARGIN=0.0
MARGIN=6
TOKEN=False
PROTO=2

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
#print("aps \n", aps)#-----------------------------------------------------------------
mss = np.zeros((param_num_nodes, 2))                                  # x, y
#print("mss \n", mss)#-----------------------------------------------------------------
asc = np.zeros((param_num_nodes)).astype(np.int)				      # ms-ap  #ms를 ap에 연결(?)
#print("asc \n", asc)#-----------------------------------------------------------------
mem = np.zeros((param_num_aps, param_num_nodes)).astype(np.int)       # connect
#print("mem \n", mem)#-----------------------------------------------------------------
dst = np.zeros((param_num_aps, param_num_channels)).astype(np.int)
#print("dst \n", dst)
dst[:, :] = -1
#print("new dst \n", dst)
chs = np.zeros((param_num_nodes, param_num_channels)).astype(np.int)  # channel
#print("chs \n", chs)
cws = np.zeros((param_num_aps, param_num_channels)).astype(np.int)    # contention window
#print("cws \n", cws)
mcw = np.zeros((param_num_aps, param_num_channels)).astype(np.int)    # maximum contention window
#print("mcw \n", mcw)
cst = np.zeros((param_num_channels))
#print("cst \n", cst)


# deploy APs -----------------------------------------------------------------
for i in range(param_num_grid):
    for j in range(param_num_grid):
        aps[i*param_num_grid+j, 0:2] = np.array([j, i]) * param_area_size + param_area_size/2
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
print("associate mss with aps")
print("asc \n", asc)
print("mem \n", mem)


# set initial CW and max CW --------------------------------------------------
for i in range(param_num_aps):
    for j in range(param_num_channels):
        mcw[i, j] = MIN_CW
        cws[i, j] = np.random.randint(mcw[i, j])
#print("mcw \n", mcw)
#print("cws \n", cws)

# set initial carrier sense threshold ----------------------------------------
for i in range(param_num_channels):
    cst[i] = param_cs_thresh
#print("cst \n", cst)


# set channels ---------------------------------------------------------------
# if param_protocol >= 0:
#     for i in range(param_num_nodes):
#         ch = i % param_num_channels
#         chs[i, ch] = 1
# print("set channels")
# print("ch \n", ch)
# print("chs \n", chs)   

#++++++++adding set channels++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print("거리에 따라 채널 할당++수신세기, interference, margin 구하기++++++++++++++++++++++")

rssilis=[]
#divind = int(param_num_nodes / param_num_channels)     #노드/channel 기준 인덱스
divind = int(param_num_nodes / 4)     #노드/4 (channel 4개 가정) 기준 인덱스
#sort -------------------
if param_protocol >= 0:   
    for i in range(param_num_aps):  
        for j in range(param_num_nodes):               
            if mem[i,j]==1:
                memind=[i,j]     #1인 index
                #print("memind", memind)
                
                # 논문에서는 거리가 아닌 RSSI 내림차순 
                myrssi = GetRxPowerDB(aps[i], mss[j])   #노드별 RSSI
                # myrssi = GetRxPowerDB_Original(mss[j], aps[i])   #RSSI 같은값나옴
                print("RSSI????", myrssi)
                
                # ---------------------------------------------------------
                # mydistance = GetDist(aps[i], mss[j])   #ap와 ms거리
                # #print("mydistance", mydistance)
                # dislis.append(mydistance)     #거리 배열
                # ---------------------------------------------------------
                
                rssilis.append(myrssi)
                rssilis = sorted(rssilis, reverse=True)   #RSSI 내림차순
print("rssilis", rssilis) 
# print("divind", divind)    
           
#set channels -------------- 채널 4개 가정
if param_protocol >= 0:   
    for i in range(param_num_aps):  
        for j in range(param_num_nodes):               
            if mem[i,j]==1:
                memind=[i,j]     #1인 index
                print("채널 memind", memind)
                # print("채널 memind", '[', i,j, ']')  #1인 index
                myrssi = GetRxPowerDB(aps[i], mss[j])   #노드별 RSSI
                print("myrssi", myrssi)                
                
                if rssilis[divind-1] <= myrssi :
                    ch=0
                    print("ch==0", ch)                                
                    
                elif rssilis[divind*2-1] <= myrssi :
                    ch=1
                    print("ch==1", ch)
                                                      
                elif rssilis[divind*3-1] <= myrssi :
                    ch=2
                    print("ch==2", ch)
                                                                     
                elif rssilis[divind*4-1] <= myrssi :
                    ch=3
                    print("ch==3", ch)
                
                elif rssilis[divind*4-1] >= myrssi:  #나머지 오류처리
                    ch=3
                    print("ch==3", ch)    
                                 
                else:
                    print("error") 
                    
                print("================")
                    
                chs[j, ch] = 1              
            #else:
                #print("channel error")
               
print("new chs \n", chs)   # 거리 기준이랑 RSSI 기준 채널 같음
#print("채널", ch)   
print("RSSI 기준=", rssilis[divind-1], rssilis[divind*2-1], rssilis[divind*3-1], rssilis[divind*4-1]) #RSSI기준
# print("거리기준=", dislis[divind-1], dislis[divind*2-1], dislis[divind*3-1], dislis[divind*4-1]) #채널기준들

#++++++++adding set channels++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

  
# select initial destination -------------------------------------------------
for c in range(param_num_channels):
    for i in range(param_num_aps):
        for j in range(param_num_nodes):
            if mem[i, j] == 1 and chs[j, c] == 1: #ap&nd and ch&nd
                dst[i, c] = j  #node
                break      
print("dst \n", dst)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++adding


# 채널별 가장 작은 received signal strength 찾기 == 채널별 AP에서 가장 거리가 먼 노드
# Ch0 => rssilis[divind-1]  // rssi로 memind 어떻게 찾음?? => 거리로 찾기(야매)
# Ch1 => rssilis[divind*2-1]
# Ch2 => rssilis[divind*3-1]
# Ch3 => rssilis[divind*4-1]

distlis=[]
divind_dist = int(param_num_nodes / 4)     #노드/4 (channel 4개 가정) 기준 인덱스
#sort -------------------
if param_protocol >= 0:   
    for i in range(param_num_aps):  
        for j in range(param_num_nodes):               
            if mem[i,j]==1:
                memind=[i,j]     #1인 index
                #print("memind", memind)
                mydistance = GetDist(aps[i], mss[j])     #ap와 ms거리
                #print("mydistance", mydistance)
                distlis.append(mydistance)     #거리 배열
                distlis = sorted(distlis)     #거리 배열 정렬 오름차순
print("distlis", distlis) 
# print("divind", divind)    

print("거리기준=\n", "ch0가장먼", distlis[divind_dist-1], "\n ch1가장먼", distlis[divind_dist*2-1], 
      "\n ch2가장먼", distlis[divind_dist*3-1], "\n ch3가장먼", distlis[param_num_nodes-1]) #채널기준들
# Ch0 => min_ch0_dist = distlis[divind_dist-1]    //거리로 찾기(야매)
# Ch1 => min_ch1_dist = distlis[divind_dist*2-1]
# Ch2 => min_ch2_dist = distlis[divind_dist*3-1]
# Ch3 => min_ch3_dist = distlis[divind_dist*4-1]


# 채널별 가장 거리가 긴 노드 = 채널별 RSSI가 작은 노드 
min_ch0_dist = distlis[divind_dist-1]    
min_ch1_dist = distlis[divind_dist*2-1]
min_ch2_dist = distlis[divind_dist*3-1]
# min_ch3_dist = distlis[divind_dist*4-1]
min_ch3_dist = distlis[param_num_nodes-1]

# 채널별 Rssi가 작은 노드 
Ps0 = rssilis[divind-1]
Ps1 = rssilis[divind*2-1]
Ps2 = rssilis[divind*3-1]
Ps3 = rssilis[divind*4-1]

print("===========================================================")


# # 채널별로 CST 구하기 //내가 만든 함수 
# cst0 = CSTperChannel(Ps0)
# cst1 = CSTperChannel(Ps1)
# cst2 = CSTperChannel(Ps2)
# cst3 = CSTperChannel(Ps3)

# print ("Ch0 CST", CSTperChannel(Ps0) )
# print ("Ch1 CST", CSTperChannel(Ps1) )
# print ("Ch2 CST", CSTperChannel(Ps2) )
# print ("Ch3 CST", CSTperChannel(Ps3) )


# GetMinCSThresh 함수 이용해서 cst 구하기
cst0 = GetMinCSThresh(min_ch0_dist)
cst1 = GetMinCSThresh(min_ch1_dist)
cst2 = GetMinCSThresh(min_ch2_dist)
cst3 = GetMinCSThresh(min_ch3_dist)



# # 내가 만든 CST함수 이용해서 cst 구하기 =====================
# # 채널별로 CST 구하기
# cst0 = CSTperChannel(Ps0)
# cst1 = CSTperChannel(Ps1)
# cst2 = CSTperChannel(Ps2)
# cst3 = CSTperChannel(Ps3)

#===========================================================



print ("Ch0 CST", cst0 )
print ("Ch1 CST", cst1 )
print ("Ch2 CST", cst2 )
print ("Ch3 CST", cst3 )



#--------------------------------------------------------------------------------


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
    print(' Tx_Power            : %d' % REFERENCE_TX_POWER)
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
        print('Progress: %3d%%' % progress, end='\r')

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
                        cs = CarrierSenseAP(i, tx_vector, aps, chs, mem,dst, ch, cst0, cst1, cst2, cst3, threshold=cst[ch])
                elif param_protocol == 1:
                    cs = DSCCarrierSenseAP(i, tx_vector, dst[:, ch], aps, mss, param_margin)
                elif param_protocol == 2:
                    cs = SmartCarrierSenseAP(i, tx_vector, dst[:, ch], aps, mss, param_margin)
                elif param_protocol >= 3:
                    cs = NewCarrierSenseAP(i, tx_vector, dst[:, ch], aps, mss, param_margin )
                if cs == True:
                    blocked[i] = 1    #true-> block
        #끝 repeatedly add transmitters 끝--------------------------------------------


        # transmit packets -------------------------------------------------------
        rx_vector, rx_snr = TransmitAP(tx_vector, dst[:, ch], mss, aps)  #return rx_vector, rx_snr
        # print("rx_vector",rx_vector)
        # print("rx_snr", rx_snr)
        for i in range(len(rx_vector)):  #ap수
            if rx_vector[i] == 1:
                stat_rx_packets_ms[dst[i, ch]] += 1     #stat_rx_packets_ms 는 ms수 배열
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
