# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 08:01:21 2022

@author: A90127
"""

import tkinter as tk
#import re
#import matplotlib.pyplot as plt

from tkinter import filedialog
from tkinter import ttk
from pyperclip import copy

import dataBuild as dB
from readme import RM, frame_styles, EcardEX2
from merge import oneVatTest, twoVatTest


class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        main_frame = tk.Frame(self, bg="#84CEEB")
        #main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        #main_frame.grid_rowconfigure(0, weight=1)
        #main_frame.grid_columnconfigure(0, weight=1)
        
        self.resizable(0, 0) #禁止調整視窗大小
        self.geometry("1024x600+504+20") #調整視窗大小及位置
        self.iconbitmap('LC.ico') 
        
        self.frames = {} #準備收集所有框架
        self.data_recipe = [] #放置工卡配方資料
        self.data_schdule = [] #放置工卡進度資料
        self.data_fiber = [] #放置染單IA胚布資料
        
        #製作各頁面
        pages = (databdPage,mainPage,authorPage)
        for F in pages:
            frame = F(main_frame, self) #建立框架
            self.frames[F] = frame #將框架存入 self 裡
            frame.grid(row=0, column=0, sticky="nsew") #放置框架
        
        #製作功能表
        menubar = MenuBar(self)
        tk.Tk.config(self, menu=menubar)
        
        #將指定的框架拉到最上層
        self.show_frame(databdPage) 
    
    #顯示頁面函數
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise() 
    #跳出App函數
    def Quit_application(self):
        self.destroy()
    
        
class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="檔案", menu=menu_file)
        menu_file.add_command(label="匯入資料", command=lambda: parent.show_frame(databdPage))
        menu_file.add_separator() #分隔線
        menu_file.add_command(label="離開", command=lambda: parent.Quit_application())

        menu_main = tk.Menu(self, tearoff=0)
        self.add_cascade(label="主程式", menu=menu_main)
        menu_main.add_command(label='分析計算', command=lambda: parent.show_frame(mainPage))
        

        menu_expression = tk.Menu(self, tearoff=0)
        self.add_cascade(label="說明", menu=menu_expression)
        menu_expression.add_command(label="關於App", command=lambda: parent.show_frame(authorPage))

                
            
class GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.main_frame = tk.Frame(self, bg="#BEB2A7", height=600, width=1024)
        # self.main_frame.pack_propagate(0)
        self.main_frame.pack(fill="both", expand="true")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)


class databdPage(GUI):  # 繼承GUI
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        self.path = ['','','']

        frame1 = tk.LabelFrame(self, frame_styles, text="匯入工卡進度")
        frame1.place(relx=0.1, rely=0.15, height=75, width=800)
        button1_1 = tk.Button(frame1, text="選擇檔案", command=lambda: Load_path(self,0))
        button1_1.grid(column=0,row=0)
        button1_2 = tk.Button(frame1, text="匯入資料", command=lambda: Load_data1(self))
        button1_2.grid(column=0,row=1)
        Label1_1 = tk.Label(frame1,text='',width=100,fg='#00F')
        Label1_1.grid(column=1,row=0)
        Label1_2 = tk.Label(frame1,text='',width=100,fg='#00F')
        Label1_2.grid(column=1,row=1)
        
        frame2 = tk.LabelFrame(self, frame_styles, text="匯入工卡配方")
        frame2.place(relx=0.1, rely=0.4, height=75, width=800)
        button2_1 = tk.Button(frame2, text="選擇檔案", command=lambda: Load_path(self,1))
        button2_1.grid(column=0,row=0)
        button2_2 = tk.Button(frame2, text="匯入資料", command=lambda: Load_data2(self))
        button2_2.grid(column=0,row=1)
        Label2_1 = tk.Label(frame2,text='',width=100,fg='#00F')
        Label2_1.grid(column=1,row=0)
        Label2_2 = tk.Label(frame2,text='',width=100,fg='#00F')
        Label2_2.grid(column=1,row=1)
        
        frame3 = tk.LabelFrame(self, frame_styles, text="匯入染單IA布號")
        frame3.place(relx=0.1, rely=0.65, height=75, width=800)
        button3_1 = tk.Button(frame3, text="選擇檔案", command=lambda: Load_path(self,2))
        button3_1.grid(column=0,row=0)
        button3_2 = tk.Button(frame3, text="匯入資料", command=lambda: Load_data3(self))
        button3_2.grid(column=0,row=1)
        Label3_1 = tk.Label(frame3,text='',width=100,fg='#00F')
        Label3_1.grid(column=1,row=0)
        Label3_2 = tk.Label(frame3,text='',width=100,fg = '#00F')
        Label3_2.grid(column=1,row=1)
        
        def Load_path(self,i):
            filename = filedialog.askopenfilename()
            Labels = [Label1_1,Label2_1,Label3_1]
            Labels[i]['text'] = filename
            self.path[i] = filename
    
        def Load_data1(self):
            controller.data_schdule = dB.schdule_E(self.path[0])
            Label1_2['text'] = '資料已匯入'
            
        def Load_data2(self):
            controller.data_recipe = dB.recipe(self.path[1])
            Label2_2['text'] = '資料已匯入'

        def Load_data3(self):
            controller.data_fiber = dB.fiber_KAIA(self.path[2])
            Label3_2['text'] = '資料已匯入'
            

class mainPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        self.controller = controller
        frame1 = tk.LabelFrame(self, frame_styles, text="查詢可併染工卡")
        frame1.place(relx=0.1, rely=0.02, width=202, height=270)        
        #判斷使否為工卡形式的函數
        def Evalidate(P):
            #print(P)
            if len(P)==0:
                return True
            elif len(P)==1:
                return P=='E'
            elif len(P)<=10:
                return str.isdigit(P[1:])
            elif len(P)<=13:
                return True
            else:
                return False
        lb1_1 = tk.Label(frame1,text = '工卡號')        
        var4 = tk.StringVar()
        #限制輸入形式滿足工卡形式
        et1_1 = tk.Entry(frame1,textvariable=var4,width=18,
                         validate='key', 
                         validatecommand=(parent.register(Evalidate), '%P'))        
        lb1_2 = tk.Label(frame1,text = '併染條件',)
        def pt():
            var1.get()
            var2.get()
            var3.get()
        var1 = tk.BooleanVar()
        cb1_1 = tk.Checkbutton(frame1,text = '同型體',variable=var1,command=pt)
        var2 = tk.BooleanVar()
        cb1_2 = tk.Checkbutton(frame1,text = '同顏色',variable=var2,command=pt)
        var3 = tk.BooleanVar()
        cb1_3 = tk.Checkbutton(frame1,text = '同配方',variable=var3,command=pt)
        bt1_1 = tk.Button(frame1,text='執行',fg='#E00',command=lambda: tvpt())
        lb1_1.grid(row=0,column=0,sticky='ew')
        et1_1.grid(row=0,column=1,sticky='ew',columnspan=2)
        lb1_2.grid(row=3,column=0,sticky='ew')
        cb1_1.grid(row=4,column=0,sticky='ew')
        cb1_2.grid(row=4,column=1,sticky='ew')
        cb1_3.grid(row=4,column=2,sticky='ew')
        bt1_1.grid(row=5,column=0,sticky='ew')
        var1.set(True)
        var2.set(True)
        var3.set(False)
        
        frame2 = tk.LabelFrame(self,frame_styles,text='併染分析')
        frame2.place(relx=0.1, rely=0.48, height=274, width=202)
        lb2_1 = tk.Label(frame2,text='單管缸量')
        lb2_2 = tk.Label(frame2,text='雙管缸量')
        lb2_3 = tk.Label(frame2,text='四管缸量')
        lb2_4 = tk.Label(frame2,text='異管容差')
        def numValidate(P):
            if len(P)<=3:
                return str.isdigit(P) or P==''
            else:
                return False
        self.et2_1 = tk.Entry(frame2,width=5,justify='r',
                         validate='key', 
                         validatecommand=(parent.register(numValidate), '%P'))
        self.et2_2 = tk.Entry(frame2,width=5,justify='r',
                         validate='key', 
                         validatecommand=(parent.register(numValidate), '%P'))
        self.et2_3 = tk.Entry(frame2,width=5,justify='r',
                         validate='key', 
                         validatecommand=(parent.register(numValidate), '%P'))
        self.et2_4 = tk.Entry(frame2,width=5,justify='r',
                         validate='key', 
                         validatecommand=(parent.register(numValidate), '%P'))
        lb2_5 = tk.Label(frame2,text='kg',bg='#BEB2A7',fg='#0000BE')
        lb2_6 = tk.Label(frame2,text='kg',bg='#BEB2A7',fg='#0000BE')
        lb2_7 = tk.Label(frame2,text='kg',bg='#BEB2A7',fg='#0000BE')
        lb2_8 = tk.Label(frame2,text='kg',bg='#BEB2A7',fg='#0000BE')
        bt2_1 = tk.Button(frame2,text='不拆卡',fg='#E00',
                          command=lambda :check1(self,controller))
        bt2_2 = tk.Button(frame2,text='初階拆卡',fg='#E00',
                          command=lambda :check2(self,controller))
        bt2_3 = tk.Button(frame2,text='進階拆卡',fg='#E00',
                          command=lambda :check3(self,controller))
        lb2_1.grid(row=0,column=0,sticky='ew')
        self.et2_1.grid(row=0,column=1,sticky='ew')
        lb2_5.grid(row=0,column=2,sticky='e')
        lb2_2.grid(row=1,column=0,sticky='ew')
        self.et2_2.grid(row=1,column=1,sticky='ew')
        lb2_6.grid(row=1,column=2,sticky='e')
        lb2_3.grid(row=2,column=0,sticky='ew')
        self.et2_3.grid(row=2,column=1,sticky='ew')
        lb2_7.grid(row=2,column=2,sticky='e')
        lb2_4.grid(row=3,column=0,sticky='ew')
        self.et2_4.grid(row=3,column=1,sticky='ew')
        lb2_8.grid(row=3,column=2,sticky='e')
        bt2_1.grid(row=4,column=0,sticky='ew')
        bt2_2.grid(row=5,column=0,sticky='ew')
        bt2_3.grid(row=6,column=0,sticky='ew')
        self.et2_1.insert(0,'70')
        self.et2_2.insert(0,'170')
        self.et2_3.insert(0,'350')
        self.et2_4.insert(0,'5')
               
        frame3 = tk.LabelFrame(self, frame_styles, text="可併染工卡")
        frame3.place(relx=0.3, rely=0.02, height=550, width=600)
        head = ('工卡號','指染單號','開卡量','近似量','分布量')
        self.tv = ttk.Treeview(frame3,
                          columns=head,
                          show='headings',
                          selectmode='extended')
        tv = self.tv
        widths = [80,80,50,50,400]
        anchors = ['c','c','c','c','w',]
        # define headings, column
        for ls,w,a in zip(head,widths,anchors):
            tv.heading(ls, text=ls)
            tv.column(ls,width=w,anchor=a)
        '''
        #輸入假設工卡(方便驗證用)
        for i,row in enumerate(EcardEX2):
            tv.insert('', 'end',values=row)
        '''
        #設定y軸滑桿
        ytreescroll = tk.Scrollbar(frame3,
                                   command=tv.yview)
        tv.configure(yscrollcommand=ytreescroll.set)
        ytreescroll.pack(side="right", fill="y")
        tv.place(relheight=0.995, relwidth=0.995)
        #設定x軸滑桿
        xtreescroll = tk.Scrollbar(frame3,
                                   command=tv.xview,
                                   orient=tk.HORIZONTAL)
        tv.configure(xscrollcommand=xtreescroll.set)
        xtreescroll.pack(side="bottom", fill="x")
        #雙擊選單事件: 複製工卡號/複製指染單號
        def copyEKA(event):
            menu = tk.Menu(parent,tearoff=0)
            def copyinE():
                for item  in tv.selection():
                    item_text = tv.item(item,"values")
                card = item_text[0]
                copy(card)
            def copyinKA():
                for item  in tv.selection():
                    item_text = tv.item(item,"values")
                card = item_text[1]
                copy(card)
            menu.add_command(label='複製工卡號',command=copyinE) #點擊後複製工卡號
            menu.add_command(label='複製指染單號',command=copyinKA)
            menu.post(event.x_root, event.y_root)
        tv.bind('<Double-1>', copyEKA)
        tv.place(relheight=0.995, relwidth=0.995)
        
        def tvpt():
            #初始化
            Refresh_data()
            #工卡號
            card = var4.get()
            # 形體 顏色 配方 的布林值序列
            TF = [var1.get(), var2.get(),var3.get()]
            data = [controller.data_schdule,controller.data_recipe,controller.data_fiber]
            search = dB.search(data,card,TF)
            for row in search:
                tv.insert('', 'end', values=row)
        def Refresh_data():
            # Deletes the data in the current treeview and reinserts it.
            tv.delete(*tv.get_children())



class authorPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)        
        frame1 = tk.LabelFrame(self, frame_styles, text="開發說明")
        frame1.place(relx=0.15, rely=0.02, height=550, width=750)       
        label1 = tk.Label(frame1, font=("Verdana", 12), text=RM,bg='#BEB2A7')
        label1.pack(side="top")
        
class GUI2(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent, bg="#BEB2A7")
        self.resizable(0, 0) #prevents the app from being resized
        self.geometry("1000x300+100+20") #fixes the applications size
        self.iconbitmap('LC.ico')
        self.frame = tk.LabelFrame(self,frame_styles)
        self.frame.place(relx=0.02,rely=0.02,width=960,height=288)
        self.tv = ttk.Treeview(self.frame,
                               show='tree headings',
                               selectmode='none')
        tv = self.tv
        tv.heading('#0', text='併法', anchor='w')
        #設定y軸滑桿
        ytreescroll = tk.Scrollbar(self.frame,
                                   command=tv.yview)
        tv.configure(yscrollcommand=ytreescroll.set)
        ytreescroll.pack(side="right", fill="y")
        #設定x軸滑桿
        xtreescroll = tk.Scrollbar(self.frame,
                                   command=tv.xview,
                                   orient=tk.HORIZONTAL)
        tv.configure(xscrollcommand=xtreescroll.set)
        xtreescroll.pack(side="bottom", fill="x")
        tv.place(relheight=0.99, relwidth=0.99)
        
class check1(GUI2):
    def __init__(self,parent,controller):
        GUI2.__init__(self,parent)
        self.frame.configure(text='不拆卡併染法')
        #抓取選取的工卡資訊
        E2fib_dict = {}
        for select_item in parent.tv.selection():
            item = parent.tv.item(select_item)
            E = item['values'][0]
            fib = [ float(item['values'][2]) ]
            E2fib_dict[E] = fib
        #抓取最大缸量、兩管誤差
        vatMax = [float(parent.et2_1.get()),float(parent.et2_2.get()),float(parent.et2_3.get())]
        err = float(parent.et2_4.get())
        #計算各種選卡分管法
        merge_dict = oneVatTest(E2fib_dict,vatMax,err)
        #print(merge_dict)
        #尋找tv的欄位數
        try:
            n = max([len(merge_dict[name][1][0]) for name in merge_dict.keys()])
        except:
            n = 0
        #打開tv欄位
        self.tv.configure(columns = list(range(n)))
        #設定欄寬
        self.tv.column('#0',width=140)
        for i in range(n):
            self.tv.column(i, width=80)
        for i,name in enumerate(merge_dict.keys()):
            cards = name.split(',')        
            #卡數
            ch1 = str(len(cards))
            #管數
            ch2 = merge_dict[name][0]
            self.tv.insert('','end',text=ch1+'卡併成'+ch2+'管',iid=i,open=True)
            nlist = [len(E2fib_dict[c]) for c in cards]
            acc = [sum(nlist[:j]) for j in range(len(nlist))]
            title = ['']*n
            for c,k in zip(cards,acc):
                title[k] = c
            self.tv.insert(i,'end',values=title)
            for row in merge_dict[name][1]:
                self.tv.insert(i,'end',text=round(sum(row),2),values=list(row))

        
class check2(GUI2):
    def __init__(self,parent,controller):
        GUI2.__init__(self,parent)
        self.frame.configure(text='初階拆卡併染法')
        #抓取選取的工卡資訊
        E2fib_dict = {}
        for select_item in parent.tv.selection():
            item = parent.tv.item(select_item)
            E = item['values'][0]
            fib = [float(i) for i in item['values'][4].split(' ')]
            E2fib_dict[E] = fib
        #抓取最大缸量、兩管誤差
        vatMax = [float(parent.et2_1.get()),float(parent.et2_2.get()),float(parent.et2_3.get())]
        err = float(parent.et2_4.get())
        #計算各種選卡分管法
        merge_dict = oneVatTest(E2fib_dict,vatMax,err)
        #print(merge_dict)
        #尋找tv的欄位數
        try:
            n = max([len(merge_dict[name][1][0]) for name in merge_dict.keys()])
        except:
            n = 0
        #打開tv欄位
        self.tv.configure(columns = list(range(n)))
        #設定欄寬
        self.tv.column('#0',width=140)
        for i in range(n):
            self.tv.column(i, width=80)
        for i,name in enumerate(merge_dict.keys()):
            cards = name.split(',')        
            #卡數
            ch1 = str(len(cards))
            #管數
            ch2 = merge_dict[name][0]
            self.tv.insert('','end',text=ch1+'卡併成'+ch2+'管',iid=i,open=True)
            nlist = [len(E2fib_dict[c]) for c in cards]
            acc = [sum(nlist[:j]) for j in range(len(nlist))]
            title = ['']*n
            for c,k in zip(cards,acc):
                title[k] = c
            self.tv.insert(i,'end',values=title)
            for row in merge_dict[name][1]:
                self.tv.insert(i,'end',text=round(sum(row),2),values=list(row))
                
class check3(GUI2):
    def __init__(self,parent,controller):
        GUI2.__init__(self,parent)
        self.frame.configure(text='進階拆卡併染法')
        #抓取選取的工卡資訊
        E2fib_dict = {}
        for select_item in parent.tv.selection():
            item = parent.tv.item(select_item)
            E = item['values'][0]
            fib = [float(i) for i in item['values'][4].split(' ')]
            E2fib_dict[E] = fib
        #抓取最大缸量、兩管誤差
        vatMax = [float(parent.et2_1.get()),float(parent.et2_2.get()),float(parent.et2_3.get())]
        err = float(parent.et2_4.get())
        #計算各種選卡分管法
        merge_dict = twoVatTest(E2fib_dict,vatMax,err)
        #print(merge_dict)
        #尋找tv的欄位數
        try:
            n = max([len(merge_dict[name][1][0]) for name in merge_dict.keys()])
        except:
            n = 0
        #打開tv欄位
        self.tv.configure(columns = list(range(n)))
        #設定欄寬
        self.tv.column('#0',width=140)
        for i in range(n):
            self.tv.column(i, width=80)
        for i,name in enumerate(merge_dict.keys()):
            cards = name.split(',')        
            #卡數
            ch1 = str(len(cards))
            #管數
            ch2 = merge_dict[name][0]
            self.tv.insert('','end',text=ch1+'卡併成'+ch2+'管',iid=i,open=True)
            nlist = [len(E2fib_dict[c]) for c in cards]
            acc = [sum(nlist[:j]) for j in range(len(nlist))]
            title = ['']*n
            for c,k in zip(cards,acc):
                title[k] = c
            self.tv.insert(i,'end',values=title)
            for row in merge_dict[name][1]:
                self.tv.insert(i,'end',text=round(sum(row),2),values=list(row))

        
root = MyApp()
root.title("利勤併染分管計算App")

root.mainloop()