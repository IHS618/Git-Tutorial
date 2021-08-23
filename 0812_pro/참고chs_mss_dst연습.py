import numpy as np


aps  = np.array(
 [[ 5.,  5.],
 [15.,  5.],
 [25.,  5.],
 [ 5., 15.],
 [15., 15.],
 [25., 15.],
 [ 5., 25.],
 [15., 25.],
 [25., 25.]])

mss = np.array(
 [[19.608,  3.45 ],
 [28.508, 14.466],
 [26.174,  6.37 ],
 [ 1.221, 11.916],
 [ 6.994, 25.252],
 [ 6.212, 22.274],
 [11.765,  5.468],
 [22.306,  2.087],
 [26.56,  28.579],
 [27.934, 12.463],
 [ 0.869, 29.461],
 [10.189, 21.201],
 [10.856,  1.053],
 [25.652, 19.718],
 [22.97,  16.623],
 [26.553, 27.126],
 [ 0.313,  2.237],
 [ 7.339,  3.999],
 [20.938, 11.946],
 [26.494,  5.43 ],
 [12.975,  0.544],
 [20.743, 14.091]] )

chs = np.array([[0, 0, 1, 0],
 [0, 1, 0, 0],
 [1, 0, 0, 0],
 [0, 0, 1, 0],
 [1, 0, 0, 0],
 [0, 1, 0, 0],
 [0, 1, 0, 0],
 [0, 0, 1, 0],
 [0, 0, 1, 0],
 [0, 1, 0, 0],
 [0, 0, 0, 1],
 [0, 0, 0, 1],
 [0, 0, 0, 1],
 [0, 0, 1, 0],
 [1, 0, 0, 0],
 [0, 1, 0, 0],
 [0, 0, 0, 1],
 [1, 0, 0, 0],
 [0, 0, 0, 1],
 [1, 0, 0, 0]])

dst= np.array(
 [[17, -1, -1, 16],
 [-1,  6,  0, 12],
 [ 2, -1,  7, -1],
 [-1, -1,  3, -1],
 [-1, -1, -1, -1],
 [14,  1, 13, 18],
 [ 4,  5, -1, 10],
 [-1, -1, -1, 11],
 [-1, 15,  8, -1]])

mem=np.array(
 [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
 [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
 [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]])


print(chs)
print(dst)
print(mem)

# for ch in range(4):
#     for i in range (9):
#         for j in range(20):
            
#             if mem[i,j]==1 and chs[j,ch]==1 and dst[i,ch]==j: 
                    
#                 if  dst[i,0]>-1 and chs[j,0]==1 : #ch0 
#                     print("ap ms ch=0", i, j, ch)
                    
#                 elif  dst[i,1]>-1 and chs[j,1]==1 : #ch1
#                     print("ap ms ch=1", i, j, ch)
                    
#                 elif  dst[i,2]>-1 and chs[j,2]==1 : #ch2 
#                     print("ap ms ch=2", i, j, ch)
                    
#                 elif  dst[i,3]>-1 and chs[j,3]==1 : #ch3
#                     print("ap ms ch=3", i, j, ch)
                    
#                 else:
#                     print("22")
                    
# print("===========")
                        
# for i in range(9):
#     for j in range(20):
#         for ch in range(4):
            
#             if mem[i,j]==1 and chs[j,ch]==1: #and dst[i,ch]==j: 
                    
#                 if  dst[i,0]>-1 and chs[j,0]==1 : #ch0 
#                     print("ap ms ch=0", i, j, ch)
                    
#                 elif  dst[i,1]>-1 and chs[j,1]==1 : #ch1
#                     print("ap ms ch=1", i, j, ch)
                    
#                 elif  dst[i,2]>-1 and chs[j,2]==1 : #ch2 
#                     print("ap ms ch=2", i, j, ch)
                    
#                 elif  dst[i,3]>-1 and chs[j,3]==1 : #ch3
#                     print("ap ms ch=3", i, j, ch)
                    
#                 else:
#                     print("22")

print("===========")

for ch in range(4):                       
    for i in range(9):
        for j in range(20):
        
            
            if mem[i,j]==1 and chs[j,ch]==1: #and dst[i,ch]==j: 
                    
                if  chs[j,0]==1 and ch ==0: #ch0 
                    print("ap=", i,"ms=", j, " ch=0", ch)
                    print(aps[i])
                    
                elif  chs[j,1]==1 and ch ==1 : #ch1
                    print("ap=", i,"ms=", j, " ch=1", ch)
                    print(aps[i])
                    
                elif  chs[j,2]==1 and ch ==2: #ch2 
                    print("ap=", i,"ms=", j, " ch=2", ch)
                    print(aps[i])
                    
                elif  chs[j,3]==1 and ch ==3: #ch3
                    print("ap=", i,"ms=", j, " ch=3", ch)
                    print(aps[i])
                    
                else:
                    print("22")
            
                
                
                
                
                
                
                
                
                
                
                
                # if ch==0 and dst[i,0]==j: #ch0
                #     print("ap ms ch=0", i, j, ch)
                    
                # elif ch==1 and dst[i,1]==j: #ch1
                #     print("ap ms ch=1", i, j, ch)
                    
                # elif ch==2 and dst[i,2]==j: #ch2
                #     print("ap ms ch=2", i, j, ch)
                    
                # elif ch==3 and dst[i,3]==j: #ch3
                #     print("ap ms ch=3", i, j, ch)
                
                # else :
                #     print("22")  # 결론 protesting 2는 안됌
                    
            
            









