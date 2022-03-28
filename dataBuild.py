# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 08:30:40 2021

@author: A90127
"""

'''
從路徑csv檔建立回傳基礎資料
'''

import numpy as np
from pandas import read_csv

#判斷該資料格是否存在 ''
def isdata(d):
    NoneType = type(None)
    if type(d)==NoneType:
        return False
    elif type(d)==str and len(d)==0:
        return False
    else:
        return True
def myfunc(path):
    data = np.array(read_csv(path,low_memory=False))
    heads = np.array(read_csv(path[:-4]+'-head.csv').columns)
    return data, heads 
def schdule_E(path):
    data, heads = myfunc(path)
    subheads = ('工卡號','染單單號','表頭狀態','開卡量','型體品名','站別','刷卡日期','刷卡時間')
    inds = [i for i,t in enumerate(heads) if t in subheads]
    return data[:,inds]

def recipe(path):
    data, heads = myfunc(path)
    subheads = ('工卡號','顏色','染劑代號','配方濃度(化驗)')
    inds = [i for i,t in enumerate(heads) if t in subheads]
    return data[:,inds]


def fiber_KAIA(path):
    data, heads = myfunc(path)
    subheads = ('染單單號','布疋號','重量','狀態',)
    inds = [i for i,t in enumerate(heads) if t in subheads]
    return data[:,inds]

#根據工卡號card,條件布林值TF過濾資料data
#data: 工卡進度、工卡配方、染單胚布
#TF : 型體、顏色、配方
def search(data,card,TF):   
    #data[0]只留下胚倉加工列
    data[0] = np.array([i for i in data[0] if i[5]=='胚倉'])
    #print(data[0])
    #data[0]過濾掉結案作廢工卡
    data[0] = np.array([i for i in data[0] if i[2] not in ('結案','強迫結案','作廢') ])
    #print(data[0])
    #data[0]過濾掉已加工工卡
    data[0] = np.array([i for i in data[0] if type(i[6])==float])
    #print(data[0])
    #data[2]拉出入胚染單
    data[2] = np.array([i for i in data[2] if i[3]=='入胚'])
    
    #data[0]過濾掉不同型體
    if TF[0]:
        #從工卡進度找出該工卡的進度列
        ind = list(data[0][:,0]).index(card)
        #型體
        shape = data[0][ind,4]
        if type(shape)==float:
            #挑出無型體的 non 辨別為浮點數
            data[0] = np.array([i for i in data[0] if type(i[4])==float])
        else:
            data[0] = np.array([i for i in data[0] if i[4]==shape])
        #print(data[0])
    #data[1]過濾掉不同顏色、data[0]也跟著過濾掉不同顏色
    if TF[1]:
        #從工卡配方列找出該工卡配方列
        ind = list(data[1][:,0]).index(card)
        color = data[1][ind,1]
        data[1] = np.array([i for i in data[1] if i[1]==color])
        cards = set(data[1][:,0])
        data[0] = np.array([i for i in data[0] if i[0] in cards])
    #data[0]過濾掉不同配方
    if TF[2]:
        #data[1]過濾掉 data[0]沒有的工卡 
        cards = set(data[0][:,0])
        data[1] = np.array([i for i in data[1] if i[0] in cards])
        #找出對照工卡的配方濃度
        std_dyes = set([i[2] for i in data[1] if i[0]==card])
        std_concs = set([i[3] for i in data[1] if i[0]==card])        
        #蒐集同配方濃度的工卡
        cards = set(data[1][:,0])
        subcards = []
        for c in cards:
            mat = np.array([i for i in data[1] if i[0]==c])
            dyes = set(mat[:,2])
            concs = set(mat[:,3])
            if dyes == std_dyes and concs == std_concs:
                subcards += [c]
        data[0] = np.array([i for i in data[0] if i[0] in subcards])
    
    
    #給開卡量,胚布重序列,回傳
    def fun(mass,ls):
        grand = [sum(ls[:i]) for i in range(1,len(ls)+1)]
        prior = [i for i,j in zip(ls,grand) if j-mass<=0]
        back = [i for i,j in zip(ls,grand) if j-mass > 0]
        diff = abs(mass-sum(prior))
        check = [i for i in back if abs(mass-sum(prior)-i)<diff]
        while check:
            a = sorted(check,reverse=True)[0]
            prior += [a]
            back.remove(a)
            diff = abs(mass-sum(prior))
            check = [i for i in back if abs(mass-sum(prior)-i)<diff]
        return prior, back
    #可併染的ka單
    kas = set(data[0][:,1])
    #最終數據儲存
    final = []
    for ka in kas:
        cards = [(i[0],i[1],float(i[3])) for i in data[0] if i[1]==ka]
        back = [float(i[2]) for i in data[2] if i[0]==ka]
        for c in cards:
            prior, back = fun(c[2],back)
            final += [c+(round(sum(prior),2),prior,)]
    return final
        
    
