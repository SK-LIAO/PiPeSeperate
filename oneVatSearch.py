# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 08:23:23 2020

@author: Ed
"""

'''
依照各種染缸條件、將多個工卡下多疋布做 併成一缸的 演算法
 mutifibls : 由多張卡下的多布疋量組成的list 
 回傳分管配管陣列 ex:
|--分管1--|
|--分管2--|
|--分管3--|
|--分管4--|
'''

import numpy as np

from itertools import combinations as cb
import pipeTest as ptst

'''---小小副程式區---'''
#將數字序列fibls 拆解成兩序列 fls1 fls3 回傳 
#使滿足a. fibls = fls1 + fls2
#      b. fls1[i] = fibls[i] if i in inds
#      c. fls1[i] = 0 if i not in inds
def Dichotomy(fibls,inds):
    #挑出組碼裡的數字,其餘用0補上
    fls1 = np.array([f if i in inds else 0 for i,f in enumerate(fibls) ])
    #fls1序列的補序列
    fls2 = np.array(fibls) - fls1
    return fls1,fls2
#將多工卡胚布矩陣壓平成序列回傳
def Flatten(mutifibs):            
    fibls = []
    for ls in mutifibs:
        fibls += list(ls)
    return np.array(fibls)
'''------搜尋法區-----'''
# 併成一單管
def S(mutifibls,vatMax):
    fibls = Flatten(mutifibls)
    return ptst.STest(fibls,vatMax), np.array([fibls])

# 併成一雙管  1:1 
def D11(mutifibls,vatMax,err):
    fibls = Flatten(mutifibls)
    #挑出fibls非0的組碼,避免重複計算
    nonzero = [i for i,m in enumerate(fibls) if m>0]
    n = len(nonzero)
    #a.分管至少一疋布,因此從 n-1開始
    #b.考慮交換性,所以只到(n-1)//2
    # i:左邊管疋數 => n-i:右邊管疋數
    for i in range(n-1,(n-1)//2,-1):
        indset = cb(nonzero,i)
        #考慮兩管疋數相等的交換性,所以只需要前半的組合
        if n%2==0 and n==2*i:
            indset = list(indset)
            indset = indset[:len(indset)//2]
        for inds in indset:
            ls1, ls2 = Dichotomy(fibls,inds)
            if ptst.D11Test(ls1,ls2,vatMax,err):                
                return True, np.array([ls1,ls2])
    return False,np.array([fibls,np.zeros(len(fibls))])   
    
# 併成一四管 3:1 
def Q31(mutifibls,vatMax,err): 
    fibls = Flatten(mutifibls)
    #a.挑出fibls非0的組碼,避免重複計算
    #b.挑出在第一工卡的組碼,因為其他工卡都會被放到 3:1分管的 1分管裡面
    nonzero = [i for i,m in enumerate(fibls) if m>0 and i<len(mutifibls[0])]
    n = len(nonzero)
    #a.1分管已經有布了,因此從 n 開始
    #b.至少得有一疋布,不具交換性,所以到0
    for i in range(n,0,-1):
        indset = cb(nonzero,i)
        for inds in indset:
            ls1, ls2 = Dichotomy(fibls,inds)
            if ptst.Q31Test(ls1,ls2,vatMax,err):                
                return True, np.array([ls1,ls2])
    return False, np.array([fibls,np.zeros(len(fibls))])

# 併成一四管 2:2 
def Q22(mutifibls,vatMax,err):
    fibls = Flatten(mutifibls)
    if len(mutifibls)!=2:
        return False,np.array([fibls,np.zeros(len(fibls))])
    ls1, ls2 = Dichotomy(fibls, list(range(len(mutifibls[0])))) 
    if ptst.Q22Test(ls1,ls2,vatMax,err):                
        return True, np.array([ls1,ls2])
    return False,np.array([fibls,np.zeros(len(fibls))])

# 併成一四管 2:1:1 
#作法 先拆成 2:2 再拆成 2:(1:1)
def Q211(mutifibls,vatMax,err):
    fibls = Flatten(mutifibls)
    #a.挑出fibls非0的組碼,避免重複計算
    #b1.挑出在第一工卡的組碼,會被放到 2:(1:1)分管的 2分管裡面
    nonzero1 = [i for i,m in enumerate(fibls) if m>0.1 and i<len(mutifibls[0])]
    n1 = len(nonzero1)
    #b2.挑出不在第一工卡的組碼,會被放到 2:(1:1)分管的 (1:1)分管裡面
    nonzero2 = tuple(i for i,m in enumerate(fibls) if m>0.1 and i>=len(mutifibls[0]))
    n2 = len(nonzero2)
    #a.2:(1:1)分管的(1:1)分管已經有布了、所以從n1開始
    #b.不具有交換性,,所以到-1為止
    for i in range(n1,-1,-1):
        indset1 = cb(nonzero1,i)
        indset2 = list(cb(nonzero1,n1-i))[::-1]
        for inds1,inds2 in zip(indset1,indset2):
            lsleft, lsright = Dichotomy(fibls, inds1)
            #a.右邊(n1-i)+n2疋,每管至少1疋,所以從n1-i+n2-1開始
            #b.因為拆成1:1具有交換性,所以到(n-i-1)//2
            for j in range(n1-i+n2-1,(n1-i+n2-1)//2,-1):
                subindset = cb(inds2+nonzero2,j)
                #考慮剩下1:1等疋的交換性,只需考慮前半的組合
                if (n1-i+n2)%2==0 and n1-i+n2==2*j:
                    subindset = list(subindset)
                    subindset = subindset[:len(subindset)//2]
                for subinds in subindset:
                    lsright1, lsright2 = Dichotomy(lsright,subinds)
                    if ptst.Q211Test(lsleft,lsright1,lsright2,vatMax,err):
                        return True,np.array([lsleft,lsright1,lsright2])
    return False, np.array([fibls, np.zeros(len(fibls)), np.zeros(len(fibls))])
            
# 併成一四管 1:1:1:1
#作法 先拆成 2:2 再各自拆成 (1:1):(1:1) 
def Q1111(mutifibls,vatMax,err):
    print(mutifibls)
    fibls = Flatten(mutifibls)
    #挑出fibls非0的組碼,避免重複計算
    nonzero = [i for i,m in enumerate(fibls) if m>0]
    n = len(nonzero)
    #a.每管至少需有一疋布,拆成2:2,所以從n-2開始
    #b.考慮交換性 所以到 (n-1)//2為止
    for i in range(n-2,(n-1)//2,-1):
        indset1 = cb(nonzero,i) #左2組碼集合
        indset2 = list(cb(nonzero,n-i))[::-1] #右2組碼集合
        #考慮兩邊疋數相等的交換性,所以只需要前半的組合
        if n%2==0 and 2*i==n:
            indset1 = list(indset1)
            indset1 = indset1[:len(indset1)//2]
            indset2 = indset2[:len(indset2)//2]
        for inds1,inds2 in zip(indset1,indset2):
            lsleft, lsright = Dichotomy(fibls, inds1) 
            #a.每管至少一疋布,一邊共i疋,所以從i-1開始
            #b.考慮交換性,所以到(i-1)//2 為止
            for j in range(i-1,(i-1)//2,-1):
                subindset1 = cb(inds1,j)
                #考慮同疋數交換性,只需考慮前半部組合
                if i%2==0 and j*2==i:
                    subindset1 = list(subindset1)
                    subindset1 = subindset1[:len(subindset1)//2]
                #a.每管至少一疋布,另一邊共n-i疋,所以從n-i-1開始
                #b.考慮交換性,所以到(n-i-1)//2 為止        
                for k in range(n-i-1,(n-i-1)//2,-1):
                    subindset2 = cb(inds2,k)
                    #考慮同疋數交換性,只需考慮前半部組合
                    if (n-i)%2==0 and k*2==n-i:
                        subindset2 = list(subindset2)
                        subindset2 = subindset2[:len(subindset2)//2]
                    for subinds1,subinds2 in zip(subindset1,subindset2):
                        lsl1,lsl2 = Dichotomy(lsleft,subinds1)
                        lsr1,lsr2 = Dichotomy(lsright, subinds2)
                        if ptst.Q1111Test(lsl1,lsl2,lsr1,lsr2,vatMax,err):
                            return True,np.array([lsl1,lsl2,lsr1,lsr2])
    return False, np.array([fibls, np.zeros(len(fibls)), np.zeros(len(fibls)), np.zeros(len(fibls))])