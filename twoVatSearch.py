# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 08:29:15 2020

@author: Ed
"""

import numpy as np
from itertools import combinations as cb

import pipeTest as ptst
import oneVatSearch as oVS
from oneVatSearch import Dichotomy,Flatten

'''
將多個工卡下多疋布做 併成兩缸的 演算法
mutifibls : 由多張卡下的多布疋量組成的list
回傳兩缸分管配管陣列 ex:
|--A缸分管1--|
|--A缸分管2--|
|--B缸分管1--|
|--B缸分管2--|

'''

# 全部併成 單管+單管
def SS(mutifibls,vatMax):
    #將所有工卡下的多疋布串成一個list
    fibls = Flatten(mutifibls)
    n = len(fibls)
    for i in range(n-1,(n-1)//2,-1):
        indset = cb(range(n),i)
        if n%2==0 and 2*i==n:
            indset = list(indset)
            indset = indset[:len(indset)//2]
        for inds in indset:
            ls1, ls2 = Dichotomy(fibls,inds)
            bol1, ls1 = oVS.S([ls1],vatMax)
            bol2, ls2 = oVS.S([ls2],vatMax)
            if bol1 and bol2:
                return True, np.array([ls1,ls2])
    return False, np.array([fibls,np.zeros(n)])

# 全部併成 雙管1:1+單管
def D11S(mutifibls,vatMax,err):
    #將所有工卡下的多疋布串成一個list
    fibls = Flatten(mutifibls)
    n = len(fibls)
    #a.因為至少留一個給單管所以從n-1開始
    #b.因為雙管1:1至少要有2疋布,所以從到2為止
    for i in range(n-1,1,-1):
        indset = cb(range(n),i)
        for inds in indset:
            lsD11, lsS = Dichotomy(fibls,inds)
            bol1, lsD11 = oVS.D11([lsD11],vatMax,err)
            bol2, lsS = oVS.S([lsS],vatMax)
            if bol1 and bol2:
                return True, np.vstack([lsD11,lsS])
    return False, np.array([fibls,np.zeros(n),np.zeros(n)])
                
# 全部併成 雙管2+雙管1:1
# 作法: 工卡1或工卡2做成雙管2,丟出幾疋布給雙管1:1 雙管2做驗證 雙管1:1做搜索
def D2D11(mutifibls,vatMax,err):
    #將所有工卡下的多疋布串成一個list
    fibls = Flatten(mutifibls)
    n = len(fibls)
    #---小副程式 供下面兩種case使用----
    def myfunc(k,indprior):
        #a.雙管2至少丟一疋布給雙管1:1,所以從n1-1開始
        #b.雙管2至少留一疋布,不可交換,所以到0
        for i in range(k-1,0,-1):
            indset = cb(indprior,i)
            for inds in indset:
                lsD2, lsD11 = Dichotomy(fibls,inds)
                if ptst.D2Test(lsD2,vatMax):
                    bol, lsD11 = oVS.D11([lsD11],vatMax,err)
                    if bol:
                        return True, np.vstack([lsD2,lsD11])
        return False, np.vstack([np.array(fibls),np.zeros((2,n))])
    #---case1: 考慮第一張工卡做雙管2---
    n1 = len(mutifibls[0])
    #第一張工卡組碼
    indprior = tuple(range(n1))
    bol1, mat = myfunc(n1,indprior)
    if bol1:
        return bol1, mat
    #---case2:考慮第二張工卡做雙管2---
    n2 = len(mutifibls[1])
    #第二張工卡組碼
    indprior = tuple(range(n1,n1+n2))
    bol2, mat = myfunc(n2,indprior)
    if bol2:
        return bol2,mat
    
    return False, np.vstack([np.array(fibls),np.zeros((2,n))])

# 全部併成 雙管1:1+雙管1:1
def D11D11(mutifibls,vatMax,err):
    #將所有工卡下的多疋布串成一個list
    fibls = Flatten(mutifibls)
    n = len(fibls)
    for i in range(n-2,(n-1)//2,-1):
        indset = cb(range(n),i)
        if n%2==0 and i*2==n:
            indset = list(indset)
            indset = indset[:len(indset)//2]
        for inds in indset:
            lsD1, lsD2 = Dichotomy(fibls,inds)
            bol1, lsD1 = oVS.D11([lsD1],vatMax,err)
            if bol1:
                bol2, lsD2 = oVS.D11([lsD2],vatMax,err)
                if bol2:
                    return True, np.vstack([lsD1,lsD2])
    return False, np.array([fibls,np.zeros(n),np.zeros(n),np.zeros(n)])


            
# 全部併成 四管3:1+單管
# 作法:先拆出 3:(1+單管) 再拆出 3:1 + 單管 分別作驗證
def Q31S(mutifibls,vatMax,err):
    #將所有工卡下的多疋布串成一個list
    fibls = Flatten(mutifibls)
    n = len(fibls)
    n1 = len(mutifibls[0])
    #第一張工卡組碼
    indprior = tuple(range(n1))
    indback = tuple(range(n1,n))
    #a.第一張工卡的布可以全部放在四管的3,所以n開始
    #b.至少必需有一疋布,不可交換,所以0為止
    for i in range(n1,0,-1):
        indset1 = cb(indprior,i)
        indset2 = list(cb(indprior,n1-i))[::-1]
        for inds1,inds2 in zip(indset1,indset2):
            #拆出給四管的3 和 給四管的1及單管
            lsQ3, lsQ1S = Dichotomy(fibls,inds1)
            #a.右邊剩下n-i疋,各至少1,所以從n-i-1開始
            #b.不可交換,至少1,所以到0為止
            for j in range(n-i-1,0,-1):
                subindset = cb(inds2+indback,j)
                for subinds in subindset:
                    lsQ1, lsS = Dichotomy(lsQ1S,subinds)
                    if ptst.Q31Test(lsQ3,lsQ1,vatMax,err) and ptst.STest(lsS,vatMax):
                        return True, np.vstack([lsQ3,lsQ1,lsS])
    return False, np.vstack([np.array(fibls),np.zeros((2,n))])

# 全部併成 四管Q22+單管
# 作法:先將第一張工卡與第二張工卡丟出幾疋布驗證Q22,剩下的驗證S
def Q22S(mutifibls,vatMax,err):
    #將所有工卡下的多疋布串成一個list
    fibls = Flatten(mutifibls)
    n = len(fibls)
    n1 = len(mutifibls[0])
    n2 = len(mutifibls[1])
    #前兩張工卡組碼集
    indprior = tuple(range(n1+n2))
    #a. Q22裡至少丟1疋出去,所以n1+n2-1開始
    #b. Q22至少有2疋,所以到1
    for i in range(n1+n2-1,1,-1):
        indset = cb(indprior,i)
        for inds in indset:
            lsQ22, lsS = Dichotomy(fibls,inds)
            lsQ_1, lsQ_2 = Dichotomy(lsQ22,[i for i in inds if i<n1])
            if ptst.Q22Test(lsQ_1,lsQ_2,vatMax,err) and ptst.STest(lsS,vatMax):
                return True, np.vstack([lsQ_1,lsQ_2,lsS])
    return False, np.vstack([np.array(fibls),np.zeros((2,n))])
    
# 全部併成 四管Q211+單管
# 作法:先拆出 2:(1:1+單管) 再拆出 2:(1:1) + 單管 
# 最後拆出 2:1:1 和 單管 各自驗證
def Q211S(mutifibls,vatMax,err):
    #將所有工卡下的多疋布串成一個list
    fibls = Flatten(mutifibls)
    n = len(fibls)
    n1 = len(fibls[0])
    indprior = tuple(range(n1))
    indback = tuple(range(n1,n))
    #a.第一張工卡可以全數做Q2,所以從n1開始
    #b.至少需有1疋布,不可交換,所以到0
    for i in range(n1,0,-1):
        indset1 = cb(indprior,i)
        indset2 = list(cb(indprior,n1-i))[::-1]
        for inds1,inds2 in zip(indset1,indset2):
            lsQ2, lsQ11S = Dichotomy(fibls,inds1)
            #a.剩n-i疋,S至少1疋,所以從n-i-1開始
            #b.Q11至少要兩疋,不可交換,所以到1
            for j in range(n-i-1,1,-1):
                subindset = cb(inds2+indback,j)
                for subinds in subindset:
                    lsQ11, lsS = Dichotomy(lsQ11S,subinds)
                    if ptst.STest(lsS,vatMax):
                        #a.剩j疋,兩小管至少1疋,所以從j-1開始
                        #b.可交換,所以到(j-1)//2
                        for k in range(j-1,(j-1)//2,-1):
                            subsubindset = cb(subinds,k)
                            if j%2==0 and 2*k==j:
                                subsubindset = list(subsubindset)
                                subsubindset = subsubindset[:len(subsubindset)//2]
                            for subsubinds in subsubindset:
                                lsQ_1,lsQ_2 = Dichotomy(lsQ11,subsubinds)
                                if ptst.Q211Test(lsQ2,lsQ_1,lsQ_1,vatMax,err):
                                    return True, np.vstack([lsQ2,lsQ_1,lsQ_1,lsS])
                        
    return False, np.vstack([np.array(fibls),np.zeros((3,n))])
    
# 全部併成 四管Q1111+單管
def Q1111S(mutifibls,vatMax,err):
    #將所有工卡下的多疋布串成一個list
    fibls = Flatten(mutifibls)
    n = len(fibls)
    for i in range(n-1,3,-1):
        indset = cb(range(n),i)
        for inds in indset:
            lsQ1111, lsS = Dichotomy(fibls,inds)
            bol1, lsQ1111 = oVS.Q1111([lsQ1111],vatMax,err)
            bol2, lsS = oVS.S([lsS],vatMax)
            if bol1 and bol2:
                return True, np.vstack([lsQ1111,lsS])
    return False, np.vstack([np.array(fibls),np.zeros((4,n))])
    
# 全部併成 四管Q31+雙管D11
# 作法:先拆成 Q3:(Q1+D11) 再拆成 Q3:Q1 + D11
# 驗證Q31、搜索D11
def Q31D11(mutifibls,vatMax,err):
    #將所有工卡下的多疋布串成一個list
    fibls = Flatten(mutifibls)
    n = len(fibls)
    n1 = len(mutifibls[0])
    #第一張工卡組碼
    indprior = tuple(range(n1))
    indback = tuple(range(n1,n))
    #a.Q3可以全部由第一張工卡組成,所以n1開始
    #b.Q3至少一疋布,不可交換,所以到0
    for i in range(n1,0,-1):
        indset1 = cb(indprior,i)
        indset2 = cb(indprior,n1-i)
        for inds1,inds2 in zip(indset1,indset2):
            lsQ3, lsQ1D11 = Dichotomy(fibls,inds1)
            #a.剩下n-i疋布,D11至少2疋,所以n-i-2開始
            #b.至少要有1疋,不可交換,所以到0
            for j in range(n-i-2,0,-1):
                subindset = cb(inds2+indback,j)
                for subinds in subindset:
                    lsQ1, lsD11 = Dichotomy(lsQ1D11,subinds)
                    if ptst.Q31Test(lsQ3,lsQ1,vatMax,err):
                        bol, mat = oVS.D11([lsD11],vatMax,err)
                        if bol:
                            return True, np.vstack([lsQ3,lsQ1,mat])
        
    return False, np.vstack([np.array(fibls),np.zeros((3,n))])
    
# 全部併成 四管Q22+雙管D11
# 作法: 隨機丟出第一張第二張工卡的幾疋布 驗證Q22
# 剩下的再搜索D11
def Q22D11(mutifibls,vatMax,err):
    #將所有工卡下的多疋布串成一個list
    fibls = Flatten(mutifibls)
    n = len(fibls)
    n1 = len(mutifibls[0])
    n2 = len(mutifibls[1])
    #前兩張工卡組碼
    indprior = tuple(range(n1+n2,n))
    #前兩張公卡至少丟出1疋布,所以從n1+n2-1開始
    #至少要有兩疋布,所以到1
    for i in range(n1+n2-1,1,-1):
        indset = cb(indprior,i)
        for inds in indset:
            lsQ22, lsD11 = Dichotomy(fibls,inds)
            lsQ_1, lsQ_2 = Dichotomy(lsQ22,[i for i in inds if i<n1])
            if ptst.Q22Test(lsQ_1,lsQ_2,vatMax,err):
                bol, mat = oVS.D11([lsD11],vatMax,err)
                if bol:
                    return True, np.vstack([lsQ_1,lsQ_2,mat])
    
    return False, np.vstack([np.array(fibls),np.zeros((3,n))])

# 全部併成 四管Q211+雙管D11
# 作法: 先拆成 Q2:(Q11 + D11), 再拆成 Q2:(Q11) + D11, 搜索D11,
# 再拆成 Q2:Q1:Q1 + D11, 然後再驗證 Q211 
def Q211D11(mutifibls,vatMax,err):
    #將所有工卡下的多疋布串成一個list
    fibls = Flatten(mutifibls)
    n = len(fibls)
    n1 = len(fibls[0])
    indprior = tuple(range(n1))
    indback = tuple(range(n1,n))
    #第一張工卡可以全數做Q2,所以從n1開始
    #至少需有1疋,不可交換,所以到0
    for i in range(n1,0,-1):
        indset1 = cb(indprior,i)
        indset2 = list(cb(indprior,n1-i))[::-1]
        for inds1,inds2 in zip(indset1,indset2):
            lsQ2, lsQ11D11 = Dichotomy(fibls,inds1)
            #剩下n-i個,至少有2疋要給D11,所以n-i-2開始
            #Q11至少要有2疋,不可交換,所以到1
            for j in range(n-i-2,1,-1):
                subindset = cb(inds2+indback,j)
                for subinds in subindset:
                    lsQ11,lsD11 = Dichotomy(lsQ11D11,subinds)
                    bol, mat = oVS.D11(lsD11,vatMax,err)
                    if bol:
                        #剩下j個,Q11至少各1,所以j-1開始
                        #可交換,所以到(j-1)//2
                        for k in range(j-1,(j-1)//2,-1):
                            subsubindset = cb(subinds,k)
                            if j%2==0 and 2*k==j:
                                subsubindset = list(subsubindset)
                                subsubindset = subsubindset[:len(subsubindset)//2]
                            for subsubinds in subsubindset:
                                lsQ11_1, lsQ11_2 = Dichotomy(lsQ11,subsubinds)
                                if ptst.Q211Test(lsQ2,lsQ11_1,lsQ11_2,vatMax,err):
                                    return True, np.vstack([lsQ2,lsQ11_1,lsQ11_2,mat])
    
    return False, np.vstack([np.array(fibls),np.zeros((4,n))])

# 全部併成 四管Q1111+雙管D11
def Q1111D11(mutifibls,vatMax,err):
    #將所有工卡下的多疋布串成一個list
    fibls = Flatten(mutifibls)
    n = len(fibls)
    for i in range(n-2,3,-1):
        indset = cb(range(n),i)
        for inds in indset:
            lsQ1111, lsD11 = Dichotomy(fibls,inds)
            bol1, lsQ1111 = oVS.Q31([lsQ1111],vatMax,err)
            bol2, lsD11 = oVS.D([lsD11],vatMax,err)
            if bol1 and bol2:
                return True, np.vstack([lsQ1111,lsD11])
    
    return False, np.vstack([np.array(fibls),np.zeros((5,n))])

# 全部合併成 四管Q1111+雙管D2
# 作法: 先拆成Q1111 + D2, 檢驗D2 (*前三張工卡都有可能做成D2)
# 剩下的再搜索Q1111
def Q1111D2(mutifibls,vatMax,err):
    #將所有工卡下的多疋布串成一個list
    fibls = Flatten(mutifibls)
    n = len(fibls)
    n1 = len(mutifibls[0])
    n2 = len(mutifibls[1])
    n3 = len(mutifibls[2])
    def myfun(indprior):
        k = len(indprior)
        #a.D2至少有1疋丟出去,所以從k-1開始
        #b.D2至少有1疋,所以到0
        for i in range(k-1,0,-1):
            indset = cb(indprior,i)
            for inds in indset:
                lsD2, lsQ1111 = Dichotomy(fibls,inds)
                if ptst.D2Test(lsD2,vatMax):
                    bol, mat = oVS.Q1111([lsQ1111],vatMax,err)
                    if bol:
                        return True, np.vstack([mat,lsD2])
        return False, np.vstack([fibls,np.zeros((4,n))])
        
    indprior = tuple(range(n1))
    bol, mat = myfun(indprior)
    if bol:
        return bol, mat
    indprior = tuple(range(n1,n1+n2))
    bol, mat = myfun(indprior)
    if bol:
        return bol, mat
    indprior = tuple(range(n1+n2,n1+n2+n3))    
    return myfun(indprior)

# 全部合併成 四管Q31+雙管D2
# 作法: 先拆成 Q31+D2, 檢驗D2(*第一張工卡跟第二張工卡可能為(Q3,D2) or (D2,Q3))
# 再拆成 Q3:Q1 + D2, 檢驗 Q31 
def Q31D2(mutifibls,vatMax,err):
    fibls = Flatten(mutifibls)
    n = len(fibls)
    n1 = len(mutifibls[0])
    n2 = len(mutifibls[1])
    def myfun(indD2,indQ3):
        k1 = len(indD2)
        k2 = len(indQ3)
        #a.D2至少丟1疋出去,所以從k-1開始
        #b.D2至少留1疋,不可交換,所以到0
        for i in range(k1-1,0,-1):
            indset1 = cb(indD2,i)
            for inds1 in indset1:
                lsD2, lsQ31 = Dichotomy(fibls,inds1)
                if ptst.D2Test(lsD2,vatMax):
                    #Q3可用全部疋布,所以從k2開始
                    #Q3至少要以1疋,不可交換,所以到0
                    for j in range(k2,0,-1):
                        indset2 = cb(indQ3,j)
                        for inds2 in indset2:
                            lsQ3, lsQ1 = Dichotomy(lsQ31,inds2)
                            if ptst.Q31Test(lsQ3,lsQ1,vatMax,err):
                                return True, np.vstack([lsQ3,lsQ1,lsD2])
        return False, np.vstack([fibls,np.zeros((2,n))])
    
    indprior1 = tuple(range(n1))
    indprior2 = tuple(range(n1,n1+n2))
    bol, mat = myfun(indprior1,indprior2)
    if bol:
        return bol,mat
    return myfun(indprior2,indprior1)
                    
    
# 全部合併成 四管Q211+雙管D2
# 作法: 先拆成 Q211+D2, 檢驗D2(*第一張工卡跟第二張工卡可能為(Q2,D2) or (D2,Q2))
# 再拆成 Q2:(Q1:Q1) + D2, 然後再成成 Q2:Q1:Q1 + D2 檢驗Q211 
def Q211D2(mutifibls,vatMax,err):
    fibls = Flatten(mutifibls)
    n = len(fibls)
    n1 = len(mutifibls[0])
    n2 = len(mutifibls[1])
    def myfun(indD2,indQ2):
        k1 = len(indD2)
        k2 = len(indQ2)
        #a.D2至少丟1疋出去,所以從k-1開始
        #b.D2至少留1疋,不可交換,所以到0
        for i in range(k1-1,0,-1):
            indset1 = cb(indD2,i)
            for inds1 in indset1:
                lsD2, lsQ211 = Dichotomy(fibls,inds1)
                if ptst.D2Test(lsD2,vatMax):
                    #Q2可用全部疋布,所以從k2開始
                    #Q2至少要以1疋,不可交換,所以到0
                    for j in range(k2,0,-1):
                        indset2 = cb(indQ2,j)
                        for inds2 in indset2:
                            lsQ2, lsQ11 = Dichotomy(lsQ211,inds2)
                            #剩下n-i-j,Q11至少各1,所以從n-i-j-1開始
                            #可交換,所以到(n-i-j-1)//2
                            for k in range(n-i-j-1,(n-i-j-1)//2,-1):
                                temp = [i for i in list(range(n)) if i not in inds1+inds2]
                                subindset = cb(temp,k)
                                if (n-i-j)%2==0 and 2*k==n-i-j:
                                    subindset = list(subindset)
                                    subindset = subindset[:len(subindset)//2]
                                for subinds in subindset:
                                    lsQ11_1,lsQ11_2 = Dichotomy(lsQ11,subinds)
                                    if ptst.Q211Test(lsQ2,lsQ11_1,lsQ11_2,vatMax,err):
                                        return True, np.vstack([lsQ2,lsQ11_1,lsQ11_2,lsD2])                                    
        return False, np.vstack([fibls,np.zeros((3,n))])
    
    indprior1 = tuple(range(n1))
    indprior2 = tuple(range(n1,n1+n2))
    bol, mat = myfun(indprior1,indprior2)
    if bol:
        return bol,mat
    return myfun(indprior2,indprior1)



