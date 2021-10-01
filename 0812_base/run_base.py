#!/usr/bin/env python
import numpy as np
from downlink_base import RunSim
import sys

np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)


# parameters -------------------------------------------------------------------
g = 10	     # grid g x g
a = 100      # area size
n = 100      # number of nodes
# c = 1        # number of channels
c = 4        # number of channels
p = 0        # protocol index
cs = -82     # carrier sense threshold
end = 1000   # simulation end time
m = 6        # CST margin
# -------------------------------------------------------------------------------

#s = np.int(sys.argv[1])
s = np.int(1000)

# ======== area 100 =====================
# --------------------------------------------------
# # # ap 변화    
# for g in range(3, 4, 10): # 3*3 일때
# # for g in range(10, 20, 100):
#     a = 100/g
#     for p in range(0, 1):
#         t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                       END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#         fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d.txt' %(g, n, c, p, -cs, m, s))
#         np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f') 
        
# for g in range(4, 14, 3): # 13*13 까지
#     a = 100/g
#     for p in range(0, 1):
#         t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                       END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#         fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d.txt' %(g, n, c, p, -cs, m, s))
#         np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f')
        
# --------------------------------------------------


# # node 변화
for n in range(20, 501, 40): # 20-500
    a = 100/g
    for p in range(0, 1):
        for s in range(1000, 1010):
            t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
                                          END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
            # fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d.txt' %(g, n, c, p, -cs, m, s))
            # np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f')
     
            with open('result_node.txt', 'a') as fn:   
                print("%5d %5d %5d %5d %5d %8.2f %5d %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f"%(g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), file=fn)
        
  

# --------------------------------------------------

# #ap고정 area_size변화
# for a in range(40, 400, 5000):  # 400
#     a = a/g
#     for p in range(0, 1):
#         t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                       END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#         fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d_a%03d.txt' %(g, n, c, p, -cs, m, s, a))
#         np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f')

# for a in range(100, 401, 100):  # 10000 - 160000
#     a = a/g
#     for p in range(0, 1):
#         t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                       END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#         fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d_a%03d.txt' %(g, n, c, p, -cs, m, s, a))
#         np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f')




# =========== area 300 으로 =======================

# # # ap 변화    
# for g in range(1, 4, 10): # 3*3 일때
# # for g in range(10, 20, 100):
#     a = 300/g
#     for p in range(0, 1):
#         t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                       END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#         fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d.txt' %(g, n, c, p, -cs, m, s))
#         np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f') 
        
# for g in range(10, 41, 10): # 10*10 - 40*40 까지
#     a = 300/g
#     for p in range(0, 1):
#         t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                       END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#         fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d.txt' %(g, n, c, p, -cs, m, s))
#         np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f')
    

# --------------------------------------------------


# # node 변화
# for n in range(20, 21, 100): # 20
#     a = 300/g
#     for p in range(0, 1):
#         t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                       END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#         fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d.txt' %(g, n, c, p, -cs, m, s))
#         np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f')
        
# for n in range(100, 401, 150): # 100 250 400 
#     a = 300/g
#     for p in range(0, 1):
#         t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                       END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#         fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d.txt' %(g, n, c, p, -cs, m, s))
#         np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f')
        
# for n in range(500, 501, 100): # 500
#     a = 300/g
#     for p in range(0, 1):
#         t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                       END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#         fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d.txt' %(g, n, c, p, -cs, m, s))
#         np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f')
        
# --------------------------------------------------


#ap고정 area_size변화
# for a in range(40, 41, 100):  # 400
#     a = a/g
#     for p in range(0, 1):
#         t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                       END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#         fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d_a%03d.txt' %(g, n, c, p, -cs, m, s, a))
#         np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f')

# for a in range(100, 401, 100):  # 10000 - 160000
#     a = a/g
#     for p in range(0, 1):
#         t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
#                                       END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
#         fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d_a%03d.txt' %(g, n, c, p, -cs, m, s, a))
#         np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f')
        
