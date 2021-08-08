#!/usr/bin/env python
import numpy as np
from downlink_cst import RunSim
import sys

np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)


# parameters -------------------------------------------------------------------
g = 10	     # grid g x g
a = 10       # area size
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

for g in range(10, 20, 100):
    a = 100/g
    for p in range(0, 1):
        t, ht, lt, f, tx, rx = RunSim(NUM_GRID=g, AREA_SIZE=a, NUM_NODES=n, NUM_CH=c, PROTO=p, CS=cs, SEED=s,
                                      END=end, VERBOSE=True, IDEAL=False, LATEX=False, MARGIN=m)
        fn = str('result_g%02d_n%03d_c%02d_p%01d_cs%03d_m%02d_s%05d.txt' %(g, n, c, p, -cs, m, s))
        np.savetxt(fn, (g, a, n, c, p, cs, m, s, t, ht, lt, f, tx, rx), fmt='%.6f')

