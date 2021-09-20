import numpy as np
import random
"""
约束条件1 x，y，z三个方向的求和均值为0
无序       random.uniform
对于第i个元素 x**2+y**2+z**2 == 1 
"""


TMP = []
for i in range(99999):
    tmp = []
    for i in range(3):
        data =  random.uniform(-6,6)     ### 标注磁矩
        tmp.append(data)
    if  0.001<tmp[0]**2 + tmp[1]**2 + tmp[2]**2 - 6**2 < 0.01 :     ### 标注磁矩
        #print(tmp)
        #print(tmp[0]**2 + tmp[1]**2 + tmp[2]**2)
        TMP.append(tmp)
        #break
    else:
        pass
        
#######################setp1#########################################        
#######################setp2#########################################
testx = []
testy = []
testz = []
for i in range(99999999):
    set1=[]
    for i in range(0,6):    ### 几个元素
        data =  random.uniform(1,len(TMP))
        #print(i)
        set1.append(int(data))
    #print(set1)
    #print("----------------")
    testx = []
    testy = []
    testz = []
    for s in set1:
        testx.append(TMP[s][0])
        testy.append(TMP[s][1])
        testz.append(TMP[s][2])
        
    if  0.001<abs(np.mean(testx)) + abs(np.mean(testy))+abs(np.mean(testz)) <= 0.05:
        print(np.mean(testx))
        print(np.mean(testy))
        print(np.mean(testz))
            #print(set1)
        print("x",testx)
        print("y",testy)
        print("z",testz)
            
    else:
            #print("Nope")
        pass
        
    #break