import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import mpl_finance
import pymysql
import time
import numpy as np
import pandas as pd
import matplotlib as mp
import gzip
import math

'''
conn = pymysql.connect(
    host="localhost", user = "root",
    password="ghfkddl1",db='testdb',charset='utf8')

cur = conn.cursor()
query = "SELECT * FROM bitmex0215"

cur.execute(query)
conn.commit()
data = cur.fetchall()
'''

tic = 20
assetb = []
assett = []
assets = []
assetb.append(0)
assets.append(0)
assett.append(0)
qty = 0.02
usdt = 1000
daylen = []
stopdt = 0
lenofcandle = []
ohlc = np.array([[47417,47417,47417,47417]])
ma = 80 
safe1 = 500
safe = 200
mam1 = ma - 1
maker = -0.00025
taker = 0.0006
cutline = 0.00465
safety = []
positionl = 0
positions = 0
positionlt = 0
positionst = 0
vol = []
count = []
dfasset = []
ticcount = 0
tictime = []
pnl_b = []
pnl_s = []
pnl_b7 = []
pnl_s7 = []
totalcom = 0
totaltrading = 0
totalcut = 0
volume = 0
volume_list = []
ver3 = 1
meand1 = []
meand2 = []
meand1ma = []
meand2ma = []
mean = []
ma30_volume = []
tic = 40
ticpoint = 0
timccount = 0
start = 0
end = 35 
x = np.arange(0,end-start)
bps = []
sp = []
sps = []
bp = []
bps.append(0)
sps.append(0)
bp.append(0)
sp.append(0)
pretime = 0
price = 0
toc = 100
kk = 5
openlong = .0
closelong = 1.5
openshort = .0
closeshort = 1.5
volvol = []
std_c = []
volvol.append(0)
volume = 0
pre_n_min = 0
j = 0
k = 0
nminvol = 0
maxima = 0
minima = 0

localmax = []
minmax = []
maxmin = []
localmax.append(0)
localmaxval = []
localmaxval.append(0)
localmin = []
localminval = []
ohlc_list = []
maxcont = np.array([1])
mincont = np.array([1])
maxconts = np.array([1])
minconts = np.array([1])
size = 0
safehistory = []
countmax = 0
countmin = 0
totalmax = []
totalmin = []

for h in range(start,end):#339#535
    positiondata = np.array([1])
    positiondatas = np.array([1])
    safehistory = safehistory[-10:]
    totalcandle = 0
    stagnation = 0
    same = 0
    additional = 0
    size = 0
    daylen.append(len(assett))
    if h > start:
        ohlc = ohlc[k:]
        lenofcandle = lenofcandle[k:]
        safety = safety[2:]
    preasset = assett[-1]
    k = len(ohlc)

    rows = []
    with gzip.open('c:/BTCUSD/DATA/%03d.gz' % h,'rb') as f:
        data = f.readlines()

    for row in data:
        rows.append(row.decode('utf-8').split(','))
        
    del rows[0]
    
    rows.reverse()
    if h == start:
        pretime = float(rows[0][0])
        price = float(rows[0][4])

    #qty = max([round((usdt+assett[-1])/price,3)])
    qty = round((100)/price,3)



    #np.delete(ohlc,0)
    tps = []
    tps.append(0)
    commi = 0
    cutnum = 0
    #std_c = std_c[-100:]
    stopl = 0
    stops = 0
  
    try:
        bp.append(bp[-1] - k)
    except:
        pass
    try:
        sp.append(sp[-1] - k)
    except:
        pass
    try:
        sps.append(sps[-1] - k)
    except:
        pass
    try:
        bps.append(bps[-1] - k)
    except:
        pass

    for i, row in enumerate(rows):
        #size += float(row[3])
        j+=1
        ticcount +=1
        tictime.append(float(row[0]))
        #volume.append(float(row[3]))
        #volume += float(row[3])
        ohlc_list.append(float(row[4]))
        price = float(row[4])

        '''
        if pretime != float(row[0])//20:
            pretime = float(row[0])//20
            tic = max([10*math.log2(volume/j) ,30])
            ma = int(10*math.log(tic))
            safe = 2*ma
            volume = 0
            j = 0
        


        if row[2] == 'Buy':
            volume += float(row[3])
        if row[2] == 'Sell':
            volume -= float(row[3])
        '''

        if ticcount >= tic:
            totalcandle += 1
            try:
                tic = min([int(80000/(float(row[0]) - tictime[-10000])),800])
                tictime = tictime[-10000:]
                ma = int(20*math.log(tic))
                safe = 100

                if np.argmax(ohlc[-19:,1]) == 10:
                    localmax.append(k-10)
                    localmaxval.append(ohlc[-10,1])
                    countmax += 1
                    if positions:
                        margin -= localmaxval - sprice
                    if localminval:
                        minmax.append((localmaxval[-1] - localminval[-1]))
                        if len(minmax) > 2:
                            if sum(minmax)/len(minmax)*1.5 > minmax[-1]:
                                if safehistory[-9] > 0:
                                    maxcont = np.append(maxcont,(localmaxval[-1]-mean[-9])*np.mean(candlestd[-ma-9:-9])/(std_c[-9]*np.std(ohlc[-ma-9:-9])))
                                else:
                                    maxconts = np.append(maxconts,(localmaxval[-1]-mean[-9])*np.mean(candlestd[-ma-9:-9])/(std_c[-9]*np.std(ohlc[-ma-9:-9])))
                            else:
                                totalmax.append(countmax)
                                countmax = 0


                if np.argmin(ohlc[-19:,2]) == 10:
                    localmin.append(k-10)
                    localminval.append(ohlc[-10,2])
                    countmin += 1
                    if positionl:
                        margin -= bprice - localminval
                    if localmaxval:
                        maxmin.append((localmaxval[-1] - localminval[-1]))
                        if len(maxmin) > 2:
                            if sum(maxmin)/len(maxmin)*1.5 > maxmin[-1]:
                                if safehistory[-9] > 0:
                                    mincont = np.append(mincont, 
                                    (-localminval[-1]+mean[-9])*np.mean(candlestd[-ma-9:-9])/(std_c[-9]*np.std(ohlc[-ma-9:-9])))
                                else:
                                    minconts = np.append(minconts,
                                    (-localminval[-1]+mean[-9])*np.mean(candlestd[-ma-9:-9])/(std_c[-9]*np.std(ohlc[-ma-9:-9])))
                            else:
                                totalmin.append(countmin)
                                countmin = 0

                
                if localmaxval[-1] > localmaxval[-2]:
                    maxima = 1
                else:
                    maxima = 0
                if localminval[-1] > localminval[-2]:
                    minima = 1
                else:
                    minima = 0

            except:
                pass
            ticcount = 0
            ticpoint = i
            if kk == 7:
                stagnation +=1

            #volume_list.append(volume)
            ohlc= np.append(ohlc,[[ohlc_list[0],max(ohlc_list),min(ohlc_list),ohlc_list[-1]]],axis=0)
            lenofcandle.append(max(ohlc_list)-min(ohlc_list))
            #lenofcandle.append(abs(ohlc_list[0]-ohlc_list[-1]))
            ohlc_list  = []
            k+=1
            if h == start:
                if k < ma:
                    continue
            candlestd = np.array(lenofcandle[-2000:])
            std_c.append(np.mean(candlestd[-ma:]))
            #aa = np.array(std_c[-20:])
            aam = np.mean(candlestd[-ma:])
            #std_c = np.std(candlestd)
            mean.append(np.mean(ohlc[-ma:,3]))
            std_p = np.std(ohlc[-ma:,3])

            std_c = std_c[-2000:]
            #bol_up = mean[-1]+std_c[-1]*meand2ma[-1]*30+ 2.5*std_p*std_c[-1]/aam
            #bol_down = mean[-1]+std_c[-1]*meand2ma[-1]*30- 2.5*std_p*std_c[-1]/aam
            if aam:
                bol_up = max([(mean[-1] + openshort*std_p*std_c[-1]/aam),price+0.5])
                bol_down =min([(mean[-1] - openlong*std_p*std_c[-1]/aam),price-0.5])
                bol_ups = max([(mean[-1] + closelong*std_p*std_c[-1]/aam),price+0.5])
                bol_downs = min([(mean[-1] - closeshort*std_p*std_c[-1]/aam),price-0.5])
            
            '''
            bol_up = mean + 14*std_c[-1]
            bol_down = mean - 14*std_c[-1]
            bol_ups = mean + 12*std_c[-1]
            bol_downs = mean - 12*std_c[-1]
            '''
            if h == start:
                if k == safe1:
                    premean = mean
                if k < safe1:
                    continue
            #safety.append(np.mean(ohlc[-safe:,3]))
            openlong = np.mean(minconts[-10:])+np.std(minconts[-10:])/2
            openshort = np.mean(maxcont[-10:])+np.std(maxcont[-10:])/2
            closelong = np.mean(maxcont[-10:])+np.std(maxcont[-10:])
            closeshort = np.mean(minconts[-10:])+np.std(minconts[-10:])

            safediffer = np.mean(ohlc[-safe:-1,3]) - np.mean(ohlc[-safe-1:-2,3])
            safehistory.append(safediffer)
            '''
            volume_list = volume_list[-100:]
            vote = np.array(volume_list)
            vote_std = (np.std(vote))
            vote_mean = (np.mean(vote))
            '''
            preminprice = price
            if np.mean(mincont[-10:]) + np.mean(maxconts[-10:]) < -1.7:
                continue

        if h == start:
            if k <= safe1+1:
                preprice = float(row[4])
                continue
        



        #=====================================================================================================
        if positionl != 0:
            if price > bol_ups >=preprice:# - cut:# > price:
                add = (price+0.5 - bprice)*qty-maker*qty*bprice-maker*qty*price
                assetb.append(add*positionl + assetb[-1])
                #if kk == 5:
                pnl_b.append(add*positionl)
                #else:
                pnl_b7.append(add*positionl)

                positionl = 0
                bps.append(k)
                tps.append(k)
                assett.append(assetb[-1]+assets[-1])
                continue
                #print(k,'BUY ',round(assetb[-1],2),round(pnl_b[-1],2),'///',round(assetb[-1]+assets[-1],2))
            #if k - bp[-1] > 2 and 10 > mean - ohlc[-3][3] > 0 and mean - ohlc[-3][3] < mean - ohlc[-1][3]:
            if bprice - price > margincut:
                add = (price-0.5 - bprice)*qty-maker*qty*bprice-taker*qty*price
                #totalmin.append(countmin)
                #countmin = 0
                assetb.append(add*positionl + assetb[-1])
                #if kk == 5:
                pnl_b.append(add*positionl)
                #else:
                pnl_b7.append(add*positionl)
                positionl = 0
                bps.append(k)
                tps.append(k)
                assett.append(assetb[-1]+assets[-1])
                commi +=taker*qty*price
                cutnum +=1
                stopl = k
                continue
                #print(k,'BUY ',round(assetb[-1],2),round(pnl_b[-1],2),'///',round(assetb[-1]+assets[-1],2),'CUT',bprice,round(price,2))
            if price - bprice > margin:
                add = (price+0.5 - bprice)*qty-maker*qty*bprice-maker*qty*price
                assetb.append(add*positionl + assetb[-1])
                #if kk == 5:
                pnl_b.append(add*positionl)
                #else:
                pnl_b7.append(add*positionl)
                positionl = 0
                bps.append(k)
                tps.append(k)
                assett.append(assetb[-1]+assets[-1])
                continue
            if safediffer < 0 and preminprice < price:
                add = (preminprice  - bprice)*qty-maker*qty*bprice-maker*qty*price
                assetb.append(add*positionl + assetb[-1])
                #if kk == 5:
                pnl_b.append(add*positionl)
                pnl_b7.append(add*positionl)
                #if pnl_b[-1] < 0:
                #    totalmin.append(countmin)
                #    countmin = 0
                bps.append(k)
                tps.append(k)
                assett.append(assetb[-1]+assets[-1])
                positionl = 0
                continue
            '''
            if localmax[-1] > bp[-1] and localmaxval[-1] > price and preminprice + 0.5 < price:
                add = (preminprice + 0.5 - bprice)*qty-maker*qty*bprice-maker*qty*price
                assetb.append(add*positionl + assetb[-1])
                #if kk == 5:
                pnl_b.append(add*positionl)
                #else:
                pnl_b7.append(add*positionl)
                bps.append(k)
                tps.append(k)
                assett.append(assetb[-1]+assets[-1])
                positionl = 0
                continue
            '''
                

        if positions != 0:
            if price < bol_downs <= preprice:# + cut:# < price:
                add = (sprice-1 - price)*qty-maker*qty*sprice-maker*qty*price
                assets.append(add*positions + assets[-1])
                #if kk == 5:
                pnl_s.append(add*positions)
                #else:
                pnl_s7.append(add*positions)
                sps.append(k)
                tps.append(k)
                positions = 0
                assett.append(assetb[-1]+assets[-1])
                #print(k,'Sell',round(assets[-1],2),round(pnl_s[-1],2),'///',round(assetb[-1]+assets[-1],2))
                continue
            if price - sprice > margincut:
                add = (sprice-0.5 - price)*qty-maker*qty*sprice-taker*qty*price
                assets.append(add*positions + assets[-1])
                #totalmax.append(countmax)
                #countmax = 0
                #if kk == 5:
                pnl_s.append(add*positions)
                #else:
                pnl_s7.append(add*positions)
                positions = 0
                sps.append(k)
                tps.append(k)
                assett.append(assetb[-1]+assets[-1])
                commi +=taker*qty*price
                cutnum +=1
                stops = k
                #print(k,'Sell',round(assets[-1],2),round(pnl_s[-1],2),'///',round(assetb[-1]+assets[-1],2),'CUT',sprice,round(price,2))
                continue
            if sprice - price > margin:
                add = (sprice-1 - price)*qty-maker*qty*sprice-maker*qty*price
                assets.append(add*positions + assets[-1])
                #if kk == 5:
                pnl_s.append(add*positions)
                #else:
                pnl_s7.append(add*positions)
                sps.append(k)
                tps.append(k)
                positions = 0
                assett.append(assetb[-1]+assets[-1])
                continue
            if safediffer > 0 and preminprice  > price:
                add = (sprice - preminprice )*qty-maker*qty*sprice-maker*qty*price
                assets.append(add*positions + assets[-1])
                #if kk == 5:
                pnl_s.append(add*positions)
                pnl_s7.append(add*positions)
                #if pnl_s[-1] < 0:
                #    totalmax.append(countmax)
                #    countmax = 0
                sps.append(k)
                tps.append(k)
                positions = 0
                assett.append(assetb[-1]+assets[-1])
                continue
            '''
            if localmin[-1] > sp[-1] and localminval[-1] < price and preminprice - 0.5 > price:
                add = (sprice - preminprice + 0.5)*qty-maker*qty*sprice-maker*qty*price
                assets.append(add*positions + assets[-1])
                #if kk == 5:
                pnl_s.append(add*positions)
                #else:
                pnl_s7.append(add*positions)
                sps.append(k)
                tps.append(k)
                positions = 0
                assett.append(assetb[-1]+assets[-1])
            '''
                
                




        if positionl == 0 and price < bol_down <= preprice:# + (k - bps[-1]):
            #if maxima ==0 and minima == 0:
            #    continue
            #if maxima == 0 and minima == 1:
            #    continue
            #if safety[-1] - safety[-2] > 0:
            if safediffer > 0:
                margin = float(sum(minmax[-10:])/len(minmax[-10:]))
                margincut = 2*sum(maxmin[-10:])/len(maxmin[-10:])
                #if margin*1.2 < minmax[-1]:
                #    continue
                positionl = 1#max([1.5 - countmin*countmin*0.02,0.5])
                bp.append(k)
                bprice = price + 0.5
                crossl = 1
                positiondata = np.append(positiondata, positionl)

        #if positions == 0 and vote_mean < 0.2:
        if positions == 0 and price > bol_up >= preprice:# - (k - sps[-1]):
            #if maxima > 0 and minima > 0:
            #    continue
            #if maxima == 0 and minima == 1:
            #    continue
            if safediffer < 0:
                margin = sum(maxmin[-10:])/len(maxmin[-10:])
                margincut = 2*sum(minmax[-10:])/len(minmax[-10:])
                #if margin*1.2 < maxmin[-1]:
                #    continue
                positions = 1#max([1.5 - countmax*countmax*0.02,0.5])
                sp.append(k)
                sprice = price - 0.5
                crosss = 1
                positiondatas = np.append(positiondata, positionl)
        
        premean = mean

        preprice = price
        #if preasset - assett[-1] > (usdt+assett[-1])*0.3:
        #    break
    totalcom +=commi
    totaltrading += len(tps)
    totalcut +=cutnum

                
    #print(time.strftime('%m-%d %H:%M:%S', time.localtime(float(data[0][0]))))
    #print(time.strftime('%m-%d %H:%M:%S', time.localtime(float(data[-1][0]))))
    vol.append((size/10000))
    count.append(len(rows))
    dfasset.append(assett[-1]-preasset)
    if len(pnl_b):
        pnlbarr = np.array(pnl_b)
        bmean = round(np.mean(pnlbarr) ,3)
        bstd = round(np.std(pnlbarr),3)
    else:
        bmean = 0
    if len(pnl_s):
        pnlsarr = np.array(pnl_s)
        smean = round(np.mean(pnlsarr) ,3)
        sstd = round(np.std(pnlsarr),3)
    else:
        smean = 0
    print(
        h,
        round(assett[-1],1),
        round(assett[-1]-preasset,1),
        '/',
        #'(',len(tps),'/',cutnum,')',#'Tic/ma',tic,ma,
        #'sametic is ', round(same/len(rows),2), kk
        #round(sum(volvol)/len(volvol),4),
        #round(stagnation/len(ohlc),3), 
        bmean,'(',bstd,')',
        smean,'(',sstd,')',
        '/',
        len(pnl_b),
        len(pnl_s),
        '/',
        round(float(rows[-1][4])/float(rows[0][4]),2),
        #round(sum(totalmax)/len(totalmax),2),round(sum(totalmin)/len(totalmin),2),
        #totalcandle, tic 
        '/',
        round(np.mean(maxcont[-10:]),2),round(np.mean(mincont[-10:]),2),
        '/',
        round(np.mean(maxconts[-10:]),2),round(np.mean(minconts[-10:]),2),
        '/',
        round(np.mean(positiondata),2),
        round(np.mean(positiondatas),2)
        )
    pnl_b = []
    pnl_s = []
pnl_b = np.array(pnl_b7)
pnl_s = np.array(pnl_s7)
mean_pnlb = np.mean(pnl_b)
std_pnlb = np.std(pnl_b)
mean_pnls = np.mean(pnl_s)
std_pnls = np.std(pnl_s)
dfdf = pd.DataFrame(count)
dfdf['assett'] = dfasset
dfdf.to_excel('result.xlsx')
print(round(mean_pnlb,3),round(mean_pnls,3),round(std_pnlb,3),round(std_pnls,3))
print(round(totalcom,2),round(totalcut/totaltrading*100,2),'%','(',totaltrading,')')
print(len(pnl_b))
print(len(pnl_s))
ohlc = pd.DataFrame(ohlc)
#ohlc.columns = ['o','h','l','c']
#ohlc['ma10'] = ohlc['c'].rolling(ma).mean()
#ohlc['ma5'] = ohlc['c'].rolling(safe).mean()
#ohlc['std'] = ohlc['c'].rolling(ma).std()
#ohlc['bol_up']=ohlc['ma10']+2*ohlc['std']
#ohlc['bol_down']=ohlc['ma10']-2*ohlc['c'].rolling(ma).std()

#daylen.append(len(assett))
dprof = []
for i in range(len(daylen)-1):
    try:
        dprof.append([
            assett[daylen[i]],
            max(assett[daylen[i]:daylen[i+1]]),
            min(assett[daylen[i]:daylen[i+1]]),
            assett[daylen[i+1]]]
            )
    except:
        dprof.append([
            assett[daylen[i]],
            assett[daylen[i]],
            assett[daylen[i]],
            assett[daylen[i]]]
        )



dfc= pd.DataFrame(count)
dfc['ma'] = dfc.rolling(10).mean()
xx = np.arange(5,end)

fig = plt.figure(figsize = (12,8))
fig.set_facecolor('w')
gs = gridspec.GridSpec(3,1, height_ratios=[3,1,1])
axes = []
axes.append(plt.subplot(gs[0]))
axes.append(plt.subplot(gs[1], sharex = axes[0]))
axes.append(plt.subplot(gs[2], sharex = axes[0]))
axes[0].get_xaxis().set_visible(False)

dprof = pd.DataFrame(dprof)
dprof.columns = ['o','h','l','c']
mpl_finance.candlestick2_ohlc(axes[0], dprof['o'],dprof['h'],dprof['l'],dprof['c'],
                              width=0.5, colorup='r', colordown='b')

axes[1].bar(x,vol,color='k', width=0.6, align='center')
axes[2].bar(x,count,color='k', width=0.6, align='center')
axes[2].plot(dfc['ma'])
'''
#PROFIC OHLC
mpl_finance.candlestick2_ohlc(axes[0], ohlc['o'],ohlc['h'],ohlc['l'],ohlc['c'],
                              width=0.5, colorup='r', colordown='b')
#axes[1].bar(x,volume_arr,color='k', width=0.6, align='center')
xx = np.arange(1,len(ohlc)+1)
axes[0].plot(xx,ohlc['ma10'],label = 'MA10')
axes[0].plot(xx,ohlc['ma5'],label = 'MA5')
axes[0].plot(x,bol_up,label = 'bol_up')
axes[0].plot(x,bol_down,label = 'bol_down')
axes[0].legend()
bps.append(len(bol_up))
sps.append(len(bol_up))
xis0= [0,0]
axes[1].plot(bps,assetb,label ='BUY($)')
axes[1].plot(tps,assett,label ='TOTAL($)')
axes[1].plot(sps,assets,label ='SELL($)')
axes[1].plot([0,len(bol_up)],xis0)
axes[1].legend()

print(ohlc.iloc[:,:4])
for i in range(len(bp)):
    axes[0].annotate(' ',xy = (bp[i],ohlc.loc[bp[i],'l']), xytext = (bp[i],ohlc.loc[bp[i],'l']-100),
                 arrowprops = dict(facecolor = 'red',shrink = 0.1, headwidth = 7, headlength = 7))
for i in range(len(bps)):
    axes[0].annotate(' ', xy = (bps[i],ohlc[bps[i],'h']), xytext = (bps[i],ohlc.loc[bps[i],'h']+100),
                 arrowprops = dict(facecolor = 'b',shrink = 0.1, headwidth = 7, headlength = 7))
'''

plt.tight_layout()
plt.show()