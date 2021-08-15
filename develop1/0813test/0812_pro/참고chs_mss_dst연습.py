import numpy as np

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
                        
for i in range(9):
    for j in range(20):
        for ch in range(4):
            
            if mem[i,j]==1 and chs[j,ch]==1: #and dst[i,ch]==j: 
                    
                if  chs[j,0]==1 : #ch0 
                    print("ap ms ch=0", i, j, ch)
                    
                elif  chs[j,1]==1 : #ch1
                    print("ap ms ch=1", i, j, ch)
                    
                elif  chs[j,2]==1 : #ch2 
                    print("ap ms ch=2", i, j, ch)
                    
                elif  chs[j,3]==1 : #ch3
                    print("ap ms ch=3", i, j, ch)
                    
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
                    
            
            









