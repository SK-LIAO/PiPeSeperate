# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 08:32:39 2020

@author: Ed

"""

'''
根據多個工卡下多疋布總重、選擇缸型最分管計算,
回傳配管字典:
工卡號字串(','連接) -> (缸型, 各管排列方式的陣列) 
'''

import numpy as np

from itertools import combinations as cb
import oneVatSearch as oVS
import twoVatSearch as tVS


#小程式(太多布疋重量重複、將陣列壓縮減少計算量)
def compression(ls):
    ls = list(ls)
    bol = True
    while bol and len(ls)>2:
        n = len(ls) 
        for i in range(n-2):
            if abs(ls[i]-ls[i+1])<0.5 and abs(ls[i]-ls[i+2])<0.5:
                ls = ls[:i+1]+ [sum(ls[i+1:i+3])] + ls[i+3:]
                break
        else:
            bol = False
    return ls

#-----只併1缸檢驗法------
#E2fib_list : 工卡號對應到胚布序列的字典
#vatMax : 各種缸型缸量上限
#err: 兩管之間最大誤差
def oneVatTest(E2fib_dict,vatMax,err):
    #壓縮胚布重量串
    for fib in E2fib_dict.keys():
        E2fib_dict[fib] = compression(E2fib_dict[fib])
    #選出所有工卡
    cards = list(E2fib_dict.keys())
    #根據工卡的重量、將工卡從新由大到小排序
    cards = sorted(cards,key = lambda x:sum(E2fib_dict[x]), reverse=True)
    merge_dict = {}
    n = len(cards)
    #可以n卡併一缸,所以從n開始
    #至少兩卡併一缸,所以到1
    for i in range(n,1,-1):
        indset = cb(range(n),i)
        for inds in indset:
            subcards = [cards[i] for i in inds]
            mutifibls = [E2fib_dict[c] for c in subcards]
            total = sum([sum(ls) for ls in mutifibls])
            if total<=vatMax[0]:
                bol, mat = oVS.S(mutifibls,vatMax)
                if bol: ch = 'S'
            elif total<=vatMax[1]:
                bol, mat = oVS.D11(mutifibls,vatMax,err)
                if bol: ch = 'D11'
            
            elif total<=vatMax[2]:
                bol, mat = oVS.Q31(mutifibls,vatMax,err)
                if bol:
                    ch = 'Q31'
                else:
                    bol, mat = oVS.Q22(mutifibls,vatMax,err)
                    if bol: 
                        ch = 'Q22'
                    else:
                        bol, mat = oVS.Q211(mutifibls,vatMax,err)
                        if bol:
                            ch ='Q211'
                            
                        else:
                            bol, mat = oVS.Q1111(mutifibls,vatMax,err)
                            if bol: 
                                ch = 'Q1111'
                        
            else:
                bol = False
            if bol:
                merge_dict[','.join(subcards)] = (ch,mat)
    return merge_dict
    
        
#-----分併兩缸檢驗法 驗完直接excel輸出-----
def twoVatTest(E2fib_dict,vatMax,err):
    #壓縮胚布重量串
    for fib in E2fib_dict.keys():
        E2fib_dict[fib] = compression(E2fib_dict[fib])
    cards = list(E2fib_dict.keys())
    #根據工卡的重量、將工卡從新由大到小排序
    cards = sorted(cards,key = lambda x:sum(E2fib_dict[x]), reverse=True)
    merge_dict = {}
    n = len(cards)
    #可以n卡併一缸,所以從n開始
    #至少3卡併兩缸,所以到2
    for i in range(n,2,-1):
        indset = cb(range(n),i)
        for inds in indset:
            subcards = [cards[i] for i in inds]
            mutifibls = [E2fib_dict[c] for c in subcards]
            total = sum([sum(ls) for ls in mutifibls])
            if total<=vatMax[0]:
                bol = False
            elif total<=vatMax[0]*2:
                bol, mat = tVS.SS(mutifibls,vatMax,err)
                if bol:
                    ch = 'SS'
            elif total<=vatMax[0]+vatMax[1]:
                bol, mat = tVS.D11S(mutifibls,vatMax,err)
                if bol:
                    ch = 'D11S'
            elif total<=vatMax[0]+vatMax[2]:
                bol, mat = tVS.D2D11(mutifibls,vatMax,err)
                if bol:
                    ch = 'D2D11'
                else:
                    bol, mat = tVS.D11D11(mutifibls,vatMax,err)
                    if bol:
                        ch = 'D11D11'
                    else:
                        bol, mat = tVS.Q31S(mutifibls,vatMax,err)
                        if bol:
                            ch = 'Q31S'
                        else:
                            bol, mat = tVS.Q22S(mutifibls,vatMax,err)
                            if bol:
                                ch = 'Q22S'
                            else:
                                bol, mat = tVS.Q211S(mutifibls,vatMax,err)
                                if bol:
                                    ch = 'Q211S'
                                else:
                                    bol, mat = tVS.Q1111S(mutifibls,vatMax,err)
                                    if bol:
                                        ch = 'Q1111S'
            elif total<=vatMax[1]+vatMax[2]:
                bol, mat = tVS.Q31D2(mutifibls,vatMax,err)
                if bol:
                    ch = 'Q31D2'
                else:
                    bol,mat = tVS.Q31D11(mutifibls,vatMax,err)
                    if bol:
                        ch = 'Q31D11'
                    else:
                        bol,mat = tVS.Q22D11(mutifibls,vatMax,err)
                        if bol:
                            ch = 'Q22D11'
                        else:
                            bol, mat = tVS.Q211D2(mutifibls,vatMax,err)
                            if bol:
                                ch = 'Q211D2'
                            else:
                                bol,mat = tVS.Q211D11(mutifibls,vatMax,err)
                                if bol:
                                    ch = 'Q211D11'
                                else:
                                    bol,mat = tVS.Q1111D2(mutifibls,vatMax,err)
                                    if bol:
                                        ch = 'Q1111D2'
                                    else:
                                        bol,mat = tVS.Q1111D11(mutifibls,vatMax,err)
                                        if bol:
                                            ch = 'Q1111D11'
            else:
                bol = False
            if bol:
                merge_dict[','.join(subcards)] = (ch,mat)
    return merge_dict 
                
