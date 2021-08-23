import matplotlib.pyplot as plt
import numpy as np

# Number of Nodes //a==100
ba1 = open("ch_node_a100_bs/result_g10_n020_c04_p0_cs082_m06_s01000.txt", "r")
ba2 = open("ch_node_a100_bs/result_g10_n100_c04_p0_cs082_m06_s01000.txt", "r")
ba3 = open("ch_node_a100_bs/result_g10_n250_c04_p0_cs082_m06_s01000.txt", "r")
ba4 = open("ch_node_a100_bs/result_g10_n400_c04_p0_cs082_m06_s01000.txt", "r")
ba5 = open("ch_node_a100_bs/result_g10_n500_c04_p0_cs082_m06_s01000.txt", "r")

dis1 = open("ch_node_a100_ds/result_g10_n020_c04_p0_cs082_m06_s01000.txt","r")
dis2 = open("ch_node_a100_ds/result_g10_n100_c04_p0_cs082_m06_s01000.txt","r")
dis3 = open("ch_node_a100_ds/result_g10_n250_c04_p0_cs082_m06_s01000.txt","r")
dis4 = open("ch_node_a100_ds/result_g10_n400_c04_p0_cs082_m06_s01000.txt","r")
dis5 = open("ch_node_a100_ds/result_g10_n500_c04_p0_cs082_m06_s01000.txt","r")

cs1 = open("ch_node_a100_cs/result_g10_n020_c04_p2_cs082_m06_s01000.txt", "r")
cs2 = open("ch_node_a100_cs/result_g10_n100_c04_p2_cs082_m06_s01000.txt", "r")
cs3 = open("ch_node_a100_cs/result_g10_n250_c04_p2_cs082_m06_s01000.txt", "r")
cs4 = open("ch_node_a100_cs/result_g10_n400_c04_p2_cs082_m06_s01000.txt", "r")
cs5 = open("ch_node_a100_cs/result_g10_n500_c04_p2_cs082_m06_s01000.txt", "r")

pr1 = open("ch_node_a100_pr/result_g10_n020_c04_p0_cs082_m06_s01000.txt", "r")
pr2 = open("ch_node_a100_pr/result_g10_n100_c04_p0_cs082_m06_s01000.txt", "r")
pr3 = open("ch_node_a100_pr/result_g10_n250_c04_p0_cs082_m06_s01000.txt", "r")
pr4 = open("ch_node_a100_pr/result_g10_n400_c04_p0_cs082_m06_s01000.txt", "r")
pr5 = open("ch_node_a100_pr/result_g10_n500_c04_p0_cs082_m06_s01000.txt", "r")

# -------------

base1 = list(map(float, np.array(ba1.readlines())))
base2 = list(map(float, np.array(ba2.readlines())))
base3 = list(map(float, np.array(ba3.readlines())))
base4 = list(map(float, np.array(ba4.readlines())))
base5 = list(map(float, np.array(ba5.readlines())))

dist1 = list(map(float, np.array(dis1.readlines())))
dist2 = list(map(float, np.array(dis2.readlines())))
dist3 = list(map(float, np.array(dis3.readlines())))
dist4 = list(map(float, np.array(dis4.readlines())))
dist5 = list(map(float, np.array(dis5.readlines())))

cstt1 = list(map(float, np.array(cs1.readlines())))
cstt2 = list(map(float, np.array(cs2.readlines())))
cstt3 = list(map(float, np.array(cs3.readlines())))
cstt4 = list(map(float, np.array(cs4.readlines())))
cstt5 = list(map(float, np.array(cs5.readlines())))

prop1 = list(map(float, np.array(pr1.readlines())))
prop2 = list(map(float, np.array(pr2.readlines())))
prop3 = list(map(float, np.array(pr3.readlines())))
prop4 = list(map(float, np.array(pr4.readlines())))
prop5 = list(map(float, np.array(pr5.readlines())))

# ---------------------------------

# throughput
x = [20, 100, 250, 400, 500] 
y1 = [base1[8], base2[8], base3[8], base4[8], base5[8]] #base6[8], base7[8], base8[8], base9[8], base10[8] ]
y2 = [dist1[8], dist2[8], dist3[8], dist4[8], dist5[8]] #dist6[8], dist7[8], dist8[8], dist9[8], dist10[8] ]
y3 = [cstt1[8], cstt2[8], cstt3[8], cstt4[8], cstt5[8]] #cstt6[8], cstt7[8], cstt8[8], cstt9[8], cstt10[8] ]
y4 = [prop1[8], prop2[8], prop3[8], prop4[8], prop5[8]] #prop6[8], prop7[8], prop8[8], prop9[8], prop10[8] ]

plt.plot(x, y1, marker="*")  #base
plt.plot(x, y2, marker="*")  #dis
plt.plot(x, y3, marker="*")  #cst
plt.plot(x, y4, marker="*")  #cst

plt.title("Total throughput vs Nodes")
plt.xlabel('nodes')
plt.ylabel('total throughput')
plt.legend(['A base', 'A\' dist','B cst', 'C pro'])  

plt.show()

# ---------------------------------

# bottom 25%
x = [20, 100, 250, 400, 500] 
y1 = [base1[10], base2[10], base3[10], base4[10], base5[10]] #, base6[10], base7[10], base8[10], base9[10], base10[10] ]
y2 = [dist1[10], dist2[10], dist3[10], dist4[10], dist5[10]] #, dist6[10], dist7[10], dist8[10], dist9[10], dist10[10] ]
y3 = [cstt1[10], cstt2[10], cstt3[10], cstt4[10], cstt5[10]] #, cstt6[10], cstt7[10], cstt8[10], cstt9[10], cstt10[10] ]
y4 = [prop1[10], prop2[10], prop3[10], prop4[10], prop5[10]] #, prop6[10], prop7[10], prop8[10], prop9[10], prop10[10] ]

plt.plot(x, y1, marker="*")  #base
plt.plot(x, y2, marker="*")  #dis
plt.plot(x, y3, marker="*")  #cst
plt.plot(x, y4, marker="*")  #cst

plt.title("Bottom 25% vs Nodes")
plt.xlabel('nodes')
plt.ylabel('bottom 25%')
plt.legend(['A base', 'A\' dist','B cst', 'C pro'])  

plt.show()

# ---------------------------------

# fairness
x = [20, 100, 250, 400, 500]  
y1 = [base1[11], base2[11], base3[11], base4[11], base5[11]]#, base6[11], base7[11], base8[11], base9[11], base10[11] ]
y2 = [dist1[11], dist2[11], dist3[11], dist4[11], dist5[11]]#, dist6[11], dist7[11], dist8[11], dist9[11], dist10[11] ]
y3 = [cstt1[11], cstt2[11], cstt3[11], cstt4[11], cstt5[11]]#, cstt6[11], cstt7[11], cstt8[11], cstt9[11], cstt10[11] ]
y4 = [prop1[11], prop2[11], prop3[11], prop4[11], prop5[11]]#, prop6[11], prop7[11], prop8[11], prop9[11], prop10[11] ]

plt.plot(x, y1, marker="*")  #base
plt.plot(x, y2, marker="*")  #dis
plt.plot(x, y3, marker="*")  #cst
plt.plot(x, y4, marker="*")  #cst

plt.title("Fairness vs Nodes")
plt.xlabel('nodes')
plt.ylabel('fairness')
plt.legend(['A base', 'A\' dist','B cst', 'C pro'])  

plt.show()










ba1.close()
ba2.close()
ba3.close()
ba4.close()
ba5.close()

dis1.close()
dis2.close()
dis3.close()
dis4.close()
dis5.close()

cs1.close()
cs2.close()
cs3.close()
cs4.close()
cs5.close()

pr1.close()
pr2.close()
pr3.close()
pr4.close()
pr5.close()



