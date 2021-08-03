#!/usr/bin/env python
import numpy as np


def GetDist(a, b):  
    return np.sqrt(np.square(a[0]-b[0]) + np.square(a[1]-b[1]))


# a=[1 ,2]

# b=[2, 3]


# print(np.argmax(a))


#distance1 = np.sqrt(np.square(5) + np.square(5))
                

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

def GetPathLossDB(distance):  
    if(distance <= REFERENCE_DIST):
        return REFERENCE_LOSS
    else:
        return REFERENCE_LOSS + 10*EXPONENT_REAL*np.log10(distance/REFERENCE_DIST)
    
def GetRxPowerDB(a, b):   
    return REFERENCE_TX_POWER - GetPathLossDB(GetDist(a, b))


aa=[7 ,2]

bb=[2, 3]

c=GetRxPowerDB(aa, bb)
print(c)