import os
import re
import urllib.request

from src.IOUtil import NetIO



       
 

# print("2017/10/06"<"2017/10/07")
#exchange_node = 'BTC-e.com'
# i=2
# url = 'https://www.walletexplorer.com/wallet/'+exchange_node+'?page='+str(i)+'&format=csv'

# findStartTime(readWrite.readDataFrom(url))

#getTransactionBetweenTime(exchange_node,"2017-09-27","2017-09-19","")    

#### The Following code will download all transaction infomation of a certain wallet ######
# exchange_node = 'BTC-e.com'
# start_from = 1



# total_page =getPageNum(exchange_node)
# print(total_page)
# page = range(start_from,total_page+1)



# total_time = 0;
# for i in page:
    
#     start=time.time()
#     url = 'https://www.walletexplorer.com/wallet/'+exchange_node+'?page='+str(i)+'&format=csv'
#     local_file = "Bitcoin/"+exchange_node + str(i)+'.csv'
#     request = urllib.request.Request(url)
#     response = urllib.request.urlopen(request)  
  
#     data = response.read()
#     data = data.decode('utf-8')
#     data=data.replace('\n','')

#     pattern2 = re.compile(r'<tr><td><a href=[^>]+')

#     readWrite.writeToFile(local_file,data)
      
   
    
#     finish=time.time()
#     t = finish-start
#     total_time += t
#     #mean = total_time / (i-start_from+1)
#     mean = t
#     expect_left = (total_page - i) * mean
#     print (str(i),'tooks ', t,"secs")
    
#     print("time left:",expect_left/60,"mins")
# print('finish')
###########################################################################################33


