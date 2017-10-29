#multiPageCrawler defines functions that will do more than one http request. Besides, the information will be write to a local file


import re
import time
import os

from IOUtil import NetIO
from IOUtil import CsvIO
import IOUtil.NetIO
# return the page number of public key of a wallet
def __getKeyPageNum(wallet_id):
    url = 'https://www.walletexplorer.com/wallet/'+wallet_id+'/addresses'
    data =  NetIO.readDataFrom(url)
    pattern = re.compile(r'Page 1 / [0-9]+')

    match = re.search(pattern, data)

    num = match.group()
    num=int(num[9:])
    return num

#return a list of all public key of a wallet on page page
def __getPublicAdr(wallet_id,page=1):
    url = 'https://www.walletexplorer.com/wallet/'+wallet_id+'/addresses?page='+str(page)
    data =  NetIO.readDataFrom(url)
    flag = 0
    pattern2 = re.compile(r'<tr><td><a href=[^>]+')
    result = []
    match=True

    while match:
        match = pattern2.search(data,flag)
        if match:
            flag = int(match.span()[-1])
            sub = match.group()[26:-1]
            result.append(sub)
        else:
            break
    return result

# call this method to download all public address of a wallet given its id
def downloadAllPublicAddressOf(wallet_id, local_file="",start_page = 1, show_time = False):
    if local_file == "":
        local_file = wallet_id+".csv" # if the user doesn't provide a file to store the key, the function will generate one

    total_page = __getKeyPageNum(wallet_id)
    total_time = 0;
    for i in range(start_page, total_page + 1):
        start = time.time()
        url = 'https://www.walletexplorer.com/wallet/' + wallet_id + '/addresses?page=' + str(i)
        data = NetIO.readDataFrom(url)

        flag = 0
        pattern2 = re.compile(r'<tr><td><a href=[^>]+')
        match=True
        while match:
            match = pattern2.search(data, flag)

            if match:
                flag = int(match.span()[-1])
                sub = match.group()[26:-1]
                CsvIO.appendToFile(local_file, sub)
            else:
                break
        finish = time.time()
        t = finish-start
        total_time += t
        expect_left = (total_page - i) * t

        if show_time:
            print (str(i),'tooks ', t,"secs")
            print(total_page, "time left:",expect_left/60,"mins")


# return the total page number of transaction of a wallet
def __getPageNum(wallet_id):
    url = 'https://www.walletexplorer.com/wallet/' + wallet_id
    data = NetIO.readDataFrom(url)
    pattern = re.compile(r'Page 1 / [0-9]+')

    match = re.search(pattern, data)

    num = match.group()
    num = int(num[9:])
    return num


def __findTime(data):
    all_time = re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', data)
    start = all_time[-1]
    end = all_time[1]
    return end, start

# call this method to download all transaction history of a given wallet id
def downloadTransactionBetweenTime(wallet_id, end_time, start_time, store_path=""):  # [start_time,end_time]
    # for easily update, accuracy to date end = 2017-10-26 start = 2017-02-21. The path should be a directory instead of a file
    total_page = __getPageNum(wallet_id)
    page = range(1, total_page + 1)
    find_end = False

    if (store_path == ""):
        store_path = wallet_id + start_time + "To" + end_time
    if not os.path.exists(store_path):
        os.makedirs(store_path)

    for i in page:
        url = 'https://www.walletexplorer.com/wallet/' + wallet_id + '?page=' + str(i) + '&format=csv'

        local_file = store_path + "/" + wallet_id + str(i) + '.csv'

        data = NetIO.readDataFrom(url)

        end, start = __findTime(data)
        if (end >= start_time and end <= end_time) or (start >= start_time and start <= end_time):
            CsvIO.writeToFile(local_file, data)
        elif (end < start_time):
            break

    # a test function
def __test():
    downloadAllPublicAddressOf("00022feb0ded1f9c",start_page = 544)
    downloadTransactionBetweenTime("Btc38.com","2017-10-29","2016-12-16")

#__test()