#!/usr/bin/env python
import numpy as np
from downlink_cst import RunSim
import sys

np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)


# parameters -------------------------------------------------------------------
g = 10	     # grid g x g
a = 100      # area size
n = 100      # number of nodes
# c = 1        # number of channels
c = 4        # number of channels
p = 2        # protocol index
cs = -82     # carrier sense threshold
end = 1000   # simulation end time
m = 6        # CST margin
# -------------------------------------------------------------------------------

#s = np.int(sys.argv[1])
s = np.int(1000)

# ========================================================
# p=2로 돌리기 2222222222222222222222222222222222222222222
# ========================================================


#=================================================
# area 100 =======================================


# node 변화
# for n in range(20, 501, 40): # 20-500
#     a = 100/g
#     for p in range(2, 3):
#         for s in range(1000, 1010):
#             t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                           END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#             # fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d.txt' %(g, n, c, p, -cs, m, s))
#             # np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f')
#             with open('result_node.txt', 'a') as fn:   
#                 print("%5d %5d %5d %5d %5d %8.2f %5d %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f"%(g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), file=fn)
        


# --------------------------------------------------


# channel 변화
# for c in range(1, 10, 1): # 1-9
#     a = 100/g
#     for p in range(2, 3):
#         for s in range(1000, 1010):
#             t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                           END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#             # fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d.txt' %(g, n, c, p, -cs, m, s))
#             # np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f')     
#             with open('result_channel.txt', 'a') as fn:   
#                 print("%5d %5d %5d %5d %5d %8.2f %5d %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f"%(g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), file=fn)


# --------------------------------------------------


# ap 변화    
# for g in range(3, 14, 1): # 3*3 - 13*13 일때
#     a = 100/g
#     for p in range(2, 3):
#         for s in range(1000, 1010):
#             t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                           END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#             # fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d.txt' %(g, n, c, p, -cs, m, s))
#             # np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f') 
#             with open('result_ap.txt', 'a') as fn:   
#                 print("%5d %5d %5d %5d %5d %8.2f %5d %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f"%(g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), file=fn)
            

        
# --------------------------------------------------
 
       
#area_size변화 (ap고정)
for a in range(40, 401, 20):  # 1600 - 160000
    a = a/g
    for p in range(2, 3):
        for s in range(1000, 1010):
            t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
                                          END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
            # fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d_a%03d.txt' %(g, n, c, p, -cs, m, s, a))
            # np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f')
            with open('result_area.txt', 'a') as fn:   
                print("%5d %5d %5d %5d %5d %8.2f %5d %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f"%(g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), file=fn)
                


# =========== area 300 으로 =======================

# ap 변화    
# for g in range(3, 14, 1): # 3*3 - 13*13 일때
#     a = 300/g
#     for p in range(2, 3):
#         for s in range(1000, 1010):
#             t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                           END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#             # fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d.txt' %(g, n, c, p, -cs, m, s))
#             # np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f') 
#             with open('result_ap_300.txt', 'a') as fn:   
#                 print("%5d %5d %5d %5d %5d %8.2f %5d %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f"%(g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), file=fn)
    


# --------------------------------------------------


# node 변화
# for n in range(20, 501, 40): # 20-500
#     a = 300/g
#     for p in range(2, 3):
#         for s in range(1000, 1010):
#             t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                           END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#             # fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d.txt' %(g, n, c, p, -cs, m, s))
#             # np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f')
     
#             with open('result_node_300.txt', 'a') as fn:   
#                 print("%5d %5d %5d %5d %5d %8.2f %5d %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f"%(g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), file=fn)
        
        
        



        
        
        
        