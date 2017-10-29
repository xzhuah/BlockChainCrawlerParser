import turtle
import math
from LocalDataParser import fileParser

#The visualization file only make simple visualization on the data downloaded by the crawlers, you may need to get all the data before being able to run this

# transaction address compare
# wallet_list = getWallet.getAllWallet()
# pageNum = []
# for id in wallet_list:
#     pageNum.append(webpage.getPageNum(id))
# print("finish")
# turtle.clear()
# for i in range(0,len(pageNum)):
#     turtle.up()
#     turtle.goto(-600,(i-30)*10)
#     turtle.down()
#     turtle.color('black')
#     turtle.write(wallet_list[i])
#     turtle.color('red')
#     turtle.forward(pageNum[i]/30)
##################################




#Bitstamp daily transaction out sum visualization
def onSameDay(tran1,tran2):
    time1=tran1["time"]
    time2=tran2["time"]
    return time1[0:10]==time2[0:10]   
#print("2017-10-27 21:49:06"[0:11]=="2017-10-27 21:49:06"[0:11])
pay_for_fee , sent_to , receive_from = fileParser.classifyTransaction("../../Bitcoin")
print("reading finished",sent_to[1])


def plotDailyAmount(tran_list):
    
    dailyAmount=[]
    small = math.inf
    large = -1

    start = tran_list[0]
    counter = float(start["amount"])
    for i in range(1,len(tran_list)):
        
        if onSameDay(start,tran_list[i]):
            counter += float(tran_list[i]["amount"])
        else:
            dailyAmount.append({"time":start["time"],"amount":counter})
           
            if counter>large:
                large=counter
            if counter<small:
                small = counter
            start = tran_list[i]
            counter = float(start["amount"])
    dailyAmount.append({"time":start["time"],"amount":counter})
    print("amount sorted",small,large)
    turtle.clear()
    turtle.speed(0)
    turtle.up()
    
    turtle.goto(700,(dailyAmount[0]["amount"] - small) / (large - small) * (800.0) - 400.0)
    turtle.down()
    for i in range(len(dailyAmount)):
        #map to [-700,700] [-400,400]
        value = float(dailyAmount[i]["amount"])
        mapvalue = (value - small) / (large - small) * (800.0) - 400.0
        
        mapX = (i - 0.0)/len(dailyAmount) * (1400.0) - 700.0
        #print(mapX,mapvalue,i,value)
        turtle.goto(-mapX,mapvalue)
        if i%20==0:
            turtle.color("red")
            turtle.write(dailyAmount[i]["time"][0:10])
            
            turtle.color("black")

plotDailyAmount(sent_to)

