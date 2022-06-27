import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import os
import os.path
import pandas as pd
from sympy import *

print("csv產生常態分布圖表,請將csv檔跟執行檔放在同一目錄中")
place = input("輸入圖表標題:")

# 從csv檔取得資料，回傳每個csv檔的資料，型態是array裡面包array -> ['型號1','平均','標準差','最小標準差','原始數值'],['型號2','平均','標準差','最小標準差','原始數值'],[...
def getInfo(path = os.getcwd()):

    roots = os.walk(path)
    csvList = []
    dicList = []
    infoList = []

    # 準備export到xlsx的變數
    exinfo =[]
    sheet2 = []
    
    for parent,dirnames,filenames in roots:
        for file in filenames:
            if ".csv" in file and parent ==path:
                csvList.append(file)
    
    if csvList == []:
        print("can't find *.csv file")
        return 

    for files in csvList:
        with open(files,'r') as csvfiles:
            for file in csvfiles:
                dicList.append(eval(file))

    for i in dicList:
        # print(f"model={i['model']} ; date={i['timeStop'][0:16]} ; dbrange={i['dbRange']} ; std={np.std(i['dbnow'])} ; average ={np.mean(i['dbnow'])}")
        infoList.append([i['model'],np.mean(i['dbnow']),np.std(i['dbnow'])])
        # 從csv檔取值並整理成dataframe可以吃的array形式
        csvtemplist = [i['model'],np.mean(i['dbnow']),np.std(i['dbnow'])]
        for num in i['dbRange']:
            csvtemplist.append(num)
        csvtemplist.append(i['MIN SD'])
        csvtemplist.append(i['MAX SD'])

        # 把原始資料塞進去
        isIdentify = [i["model"],'isidentify?']
        triggerdb = []
        triggerdb.append(i['model'])
        triggerdb.append('triggerdb:mean+3SD')
        SDlist = []
        SDlist.append(i['model'])
        SDlist.append('SD')
        minSDlist = []
        minSDlist.append(i['model'])
        minSDlist.append('minSD')
        maxSDlist = []
        maxSDlist.append(i['model'])
        maxSDlist.append('maxSD')
        dbList = []
        dbList.append(i['model'])
        dbList.append('DB')

        maxdbList = []
        maxdbList.append(i['model'])
        maxdbList.append('max DB')
        mindbList = []
        mindbList.append(i['model'])
        mindbList.append('min DB')
       

        for maxdb in i['maxDB']:
            maxdbList.append(maxdb)
        
        for mindb in i['minDB']:
            mindbList.append(mindb)

        for SD in i['nowSD']:
            SDlist.append(SD)
        
        for minSD in i['minSDlist']:
            minSDlist.append(minSD)
        
        for maxSD in i['maxSDlist']:
            maxSDlist.append(maxSD)
        
        for j in i['triggerdb']:
            triggerdb.append(j)
        
        # valueB_changeto2_5 = []
        # valueB_changeto2_5.append(i['model'])
        # valueB_changeto2_5.append('coefficient B=2.5')

        # valueB_changeto2_25 = []
        # valueB_changeto2_25.append(i['model'])
        # valueB_changeto2_25.append('coefficient B=2.25')
        
        # for db in triggerdb[2:]:
        #     x = Symbol('x')
        #     solved = solve(x+2.75*((84-x)**0.5)-int(db),x)
        #     # print(type(float(solved[0])))
        #     temp = float(solved[0])+(2.5*((84-float(solved[0]))**0.5))
        #     valueB_changeto2_5.append(temp)
        #     temp = float(solved[0])+(2.25*((84-float(solved[0]))**0.5))
        #     valueB_changeto2_25.append(temp)
        
       
        # sheet2.append(valueB_changeto2_5)
        # sheet2.append(valueB_changeto2_25)


       

        # 建立2個標準差的array
        DBthreshold2σ = []
        DBthreshold2σ.append(i['model'])
        DBthreshold2σ.append("2σ")

        # 建立2.5個標準差
        DBthreshold2_5σ=[]
        DBthreshold2_5σ.append(i['model'])
        DBthreshold2_5σ.append('2.5σ') 

        # 建立3個標準差的array
        DBthreshold3σ=[]
        DBthreshold3σ.append(i['model'])
        DBthreshold3σ.append('3σ')

        for k in i['dbnow']:
            csvtemplist.append(k)   
            dbList.append(k)
        for index,db in enumerate(triggerdb[2:]):
            if db < dbList[2:][index]:
                isIdentify.append("Over threshold")
            else:
                isIdentify.append("")
        for index in range(len(i['dbnow'])):
            if index>=30:
                stdtemp = np.std(i['dbnow'][index-30:index+1])
                meantemp = np.mean(i['dbnow'][index-30:index+1])
                DBthreshold2σ.append(meantemp+stdtemp*2)
                DBthreshold2_5σ.append(meantemp+stdtemp*2.5)
                DBthreshold3σ.append(meantemp+stdtemp*3)
            else:
                DBthreshold2σ.append('')
                DBthreshold2_5σ.append('')
                DBthreshold3σ.append('')

        count2σ = 0
        count2_5σ = 0
        count3σ = 0

        for index,db in enumerate(DBthreshold2σ[2:]):
            if db!='':
                if db<dbList[2:][index]:
                    count2σ+=1

        for index,db in enumerate(DBthreshold2_5σ[2:]):
            if db!='':
                if db<dbList[2:][index]:
                    count2_5σ+=1

        for index,db in enumerate(DBthreshold3σ[2:]):
            if db!='':
                if db<dbList[2:][index]:
                    count3σ+=1

        DBthreshold2σ.append('count=')
        DBthreshold2σ.append(count2σ)
        DBthreshold2_5σ.append('count=')
        DBthreshold2_5σ.append(count2_5σ)
        DBthreshold3σ.append('count=')
        DBthreshold3σ.append(count3σ)

        
        # sheet2.append(DBthreshold2σ)
        # sheet2.append(DBthreshold3σ)

        dbTriggerTime = []
        dbTriggerTime.append("trigger time")
        dbTriggerType = []
        dbTriggerType.append("Type")

        for time in i['dbTriggerTime']:
            dbTriggerTime.append(time+2)
        for type in i['dbTriggerType']:
            dbTriggerType.append(type)

        sheet2.append(triggerdb)
        sheet2.append(dbList)
        sheet2.append(SDlist)
        sheet2.append(minSDlist)
        sheet2.append(maxSDlist)
        sheet2.append(maxdbList)
        sheet2.append(mindbList)
        sheet2.append(dbTriggerTime)
        sheet2.append(dbTriggerType)
        


        # sheet2.append(isIdentify)
        # print(sheet2)

        exinfo.append(csvtemplist)

    
    if(getInfofromDBmeter()!=None):
        dbmeterinfo = getInfofromDBmeter()
        infoList.append(dbmeterinfo[0])
        # 從slm檔取值並整理成dataframe可以吃的array形式
        DBmetertemplist = [dbmeterinfo[0][0],(dbmeterinfo[0][1]),(dbmeterinfo[0][2]),'','','']
        # 把原始資料塞進去
        for i in dbmeterinfo[1]:
            DBmetertemplist.append(i)
        exinfo.append(DBmetertemplist)
    
    # 把準備好的資料exinfo 變成dataframe的型態
    data1 = pd.DataFrame(exinfo)
    sheet2 = pd.DataFrame(sheet2)

    maxnum = 0
    columns =[]
    # 看最長那行有幾個數值，因為每個數值都要有對應的標籤
    for i in exinfo:
        maxnum = max(len(i),maxnum)
    # 新增標籤
    columns[0:6]=['model','mean','std','MIN','MAX','Min SD','Max SD','raw']
    # 把最上面那行標籤填滿
    for i in range(1,maxnum-(len(columns)-1)):
        columns.append(i)
    data1.columns=columns

    # 存成xlsx檔
    # writer = pd.ExcelWriter(f'{place}_result.xlsx')
    with pd.ExcelWriter(f"{place}_result.xlsx") as writer1:
        data1.to_excel(writer1, sheet_name=f'{place}',index = False)
        sheet2.to_excel(writer1, sheet_name='threshold info',index = False)
    # writer.save

    return infoList

# 從slm檔(DBMeter)取得資料，若有資料則在getInfo的array新增一組數據，若無則return
def getInfofromDBmeter(path = os.getcwd()):
    dbmeterlist = []
    DBMeter_InfoList = []
    roots = os.walk(path)
    DBMeter = None
    for parent,dirnames,filenames in roots:
        for file in filenames:
            if ".slm" in file and parent ==path:
                DBMeter = file
    if DBMeter == None:
        print("can't find slm file")
        return 

    with open(DBMeter,'r') as DBMeterInfo:
        for i in DBMeterInfo:
            if len(i)>25:
                # 將分貝計存的slm檔案一些多餘的換行、縮排消除
                temp = i.replace("\n","").replace("\t","")

                """
                temp = float(temp[-4:])
                此為取尾巴部分的db值
                這樣的寫法超過100db會出錯,要另外修改
                """
                temp = float(temp[-4:])
                dbmeterlist.append(temp)
        DBMeter_InfoList = ["DBMeter "+DBMeter.replace(".slm",''),np.mean(dbmeterlist),np.std(dbmeterlist)]


        return [DBMeter_InfoList,dbmeterlist]

# input:data -> output:table
def draw_normal(mu=0, sigma=1, size=10000):
    np.random.seed(0)
    dnormal = np.random.normal(mu, sigma, size)
    _, bins_edge, _ = plt.hist(dnormal, bins=50, density=True, alpha=0.2    )

    # 機率密度函數曲線
    y = scipy.stats.norm.pdf(bins_edge, mu, sigma)
    plt.plot(bins_edge, y, label='$\mu$=%.1f, $\sigma^2$=%.1f'%(mu, sigma))

    return True


# 將資料餵進draw_normal及繪製圖表邊框
def show_normal_dist_plot(data,location):
    model = []
    for i in data:
        draw_normal(mu=i[1],sigma=i[2])
        # 若重複型號則加上 2 的標記
        if i[0] in model:
            temp = [i[0]+" 2","mean = "+str(round(i[1],2))]
            model.append(temp)
        else:
            temp = [i[0],"mean = "+str(round(i[1],2))]
            model.append(temp)

    plt.legend(model)
    plt.title(location)
    plt.xlabel('dB')
    plt.ylabel('Probability')
    plt.savefig(f'{place}.png', dpi=200)
    plt.show()
    

data = getInfo()
# print(data)
if data != None:
    show_normal_dist_plot(data,place)