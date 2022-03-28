# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 08:16:31 2020

@author: Ed
"""

from itertools import combinations as cb


'''
-------------合併條件測試區------------
測試各種缸型分管方式是否符合條件
符合條件符合 回傳 True,不符合回傳 False
''' 
#vatMax : 單管、雙管、四管的缸量上限 陣列缸 
#err : 異管容差

# 單管的測試
def STest(l1,vatMax): 
    return sum(l1) <= vatMax[0]
        
# 雙管的 2 分管測試
def D2Test(l1,vatMax): 
    return vatMax[0]< sum(l1) <=vatMax[1]

# 雙管的 1:1 分管測試
def D11Test(l1,l2,vatMax,err): 
    m1 = sum(l1)
    m2 = sum(l2)
    return abs(m1-m2)<=err and vatMax[0]< m1+m2 <=vatMax[1]

# 四管的 4 分管測試
def Q4Test(l1,vatMax):
    return vatMax[1]< sum(l1) <=vatMax[2]

# 四管的 3:1 分管測試
def Q31Test(l1,l2,vatMax,err): 
    m1 = sum(l1)
    m2 = sum(l2)
    return abs(m1/3-m2)<=err and vatMax[1]<m1+m2<=vatMax[2]

# 四管的 2:2 分管測試
def Q22Test(l1,l2,vatMax,err):
    m1 = sum(l1)
    m2 = sum(l2)
    return abs(m1/2-m2/2)<=err and vatMax[1]<m1+m2<=vatMax[2]

# 四管的 2:1:1 分管測試    
def Q211Test(l1,l2,l3,vatMax,err): 
    mls = [sum(l1)/2,sum(l2),sum(l3)]
    bols = [abs(i[0]-i[1])<=err for i in cb(mls,2)]
    return all(bols) and vatMax[1]<sum(mls)<=vatMax[2]

# 四管的 1:1:1:1 分管測試
def Q1111Test(l1,l2,l3,l4,vatMax,err): 
    mls = [sum(l1), sum(l2), sum(l3), sum(l4)]
    bols = [abs(i[0]-i[1])<=err for i in cb(mls,2)]
    return all(bols) and vatMax[1]<sum(mls)<=vatMax[2]