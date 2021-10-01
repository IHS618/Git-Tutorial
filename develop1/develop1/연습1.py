#!/usr/bin/env python
import numpy as np

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

param_num_aps=9
param_num_grid=3
param_num_nodes_per_cell=1
aps = np.zeros((param_num_aps, 2)) 
param_area_size=10
param_num_nodes=9
NUM_NODES=0
mss = np.zeros((param_num_nodes, 2))
  
if NUM_NODES == 0:
        param_num_nodes = param_num_aps*param_num_nodes_per_cell
else:
        param_num_nodes = NUM_NODES
    
for i in range(param_num_grid):
        for j in range(param_num_grid):
            aps[i*param_num_grid+j,0:2] = np.array([j, i]) * param_area_size + param_area_size/2
            
if NUM_NODES == 0:
        for i in range(param_num_aps):
            for j in range(param_num_nodes_per_cell):
                base = (np.random.rand(2)*2-1)*param_area_size/2
                ind = i * param_num_nodes_per_cell + j
                mss[ind, 0:2] = aps[i] + base
                
        
print(aps)
print(aps.shape[0]) 

print("mss")
print(mss) 

ms=[23,24]
a=GetNearestAP(ms, aps)
print(a)



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

tx_vector = np.zeros(param_num_aps)

print("txv")
print(tx_vector)
tx_dest=8
v, s = TransmitAP(tx_vector, tx_dest, mss, aps)
print("result")
print(v,s)


