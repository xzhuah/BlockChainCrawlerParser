# singlePageCrawler defined a set of realtime function that will do at most one http request, the data will only be stored in memory
from crawlerUtil import str2Object
from crawlerUtil import find_between
import re

from bs4 import BeautifulSoup
from src.IOUtil import NetIO



# The following functions are designed for using the API on https://blockchain.info/api/blockchain_api

def blockQuery(block_hash):
    url = "https://blockchain.info/rawblock/" + block_hash
    return str2Object(NetIO.readDataFrom(url))


def transactionQuery(tx_hash):
    url = "https://blockchain.info/rawtx/" + tx_hash
    return str2Object(NetIO.readDataFrom(url))


def blockHeight(block_height):
    url = "https://blockchain.info/block-height/" + block_height + "?format=json"
    return str2Object(NetIO.readDataFrom(url))


def balanceQuery(address):
    # Multiple Addresses Allowed separated by "|" , Address can be base58 or xpub
    url = "https://blockchain.info/balance?active=" + address
    return str2Object(NetIO.readDataFrom(url))


def addressQuery(address):
    url = "https://blockchain.info/rawaddr/" + address
    return str2Object(NetIO.readDataFrom(url))


def addressesQuery(addresses):
    query = ''
    for add in addresses:
        query += add + "|"
    url = "https://blockchain.info/multiaddr?active=" + query[0:-1]
    return str2Object(NetIO.readDataFrom(url))


def unspentOutput(address, limit=250, confirmNum=6):
    # Multiple Addresses Allowed separated by "|" , Address can be base58 or xpub

    if limit > 1000:
        limit = 1000
    url = "https://blockchain.info/unspent?active=" + address + "&limit=" + str(limit) + "&confirmations=" + str(
        confirmNum)
    return str2Object(NetIO.readDataFrom(url))



def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""
###################################################
        # The following function will read data from www.walletexplorer.com

# query transaction from walletExplorer
  #
    # {
    #     "txid": ,
    #     "block":,
    #     "time":,
    #     "sender":,
    #     "fee":,
    #     "input":[{"key":value,"amount":value,"prev":value},{"key":value}],
    #     "output":{{"receiver1":[{"key",value,"amount":value,"next":}],"receiver2":[{},{}]}}
    # }

# return an object of transaction given transaction id
def transactionWalletQuery(txid):
    result = {}
    rawdata = NetIO.readDataFrom("https://www.walletexplorer.com/txid/" + txid)
    soup = BeautifulSoup(rawdata, "lxml")
    # soup.find('table',class_="info")
    info = soup.find('table', class_="info").get_text()
    # print(info)
    pattern_block = re.compile(r"block[0-9]+")
    pattern_time = re.compile(r"Time[^a-z]+")

    block = int(pattern_block.search(info).group()[5:])
    time = pattern_time.search(info).group()
    sender = find_between(info, "Sender", "Fee")

    fee = float(find_between(info, "Fee", "BTC"))
    # print(block,time,sender,fee)
    result["block"] = block
    result["time"] = time
    result["sender"] = sender
    result["fee"] = fee
    result["txid"] = txid

    inout = soup.find_all('table', class_="empty")
    inAddress = inout[0]
    outAddress = inout[1]

    all_line = inAddress.find_all("tr")
    input_list = []
    for line in all_line:
        cols = line.find_all("td")
        public_add = cols[0].find('a').get_text()
        value = float(find_between(">" + cols[1].get_text(), ">", "BTC"))

        pre = find_between(str(cols[2]), "txid/", '">')
        input_list.append({"key": public_add, "amount": value, "prev": pre})
    result["input"] = input_list
    all_line = outAddress.find_all("tr")
    my_set = {}
    for line in all_line:
        cols = line.find_all("td")
        public_add = cols[0].find('a').get_text()
        wallet_id = find_between(str(cols[1]), "wallet/", '">')

        value = float(find_between(">" + cols[2].get_text(), ">", "BTC"))
        next = find_between(str(cols[3]), "/txid/", '">')
        if next == "":
            next = "NONE"
        if wallet_id in my_set:
            my_set[wallet_id].append({"key": public_add, "amount": value, "next": next})
        else:
            my_set[wallet_id] = [{"key": public_add, "amount": value, "next": next}]

    result["output"] = my_set
    return result

# return the wallet id that the public address belongs to
def findWalletByAddre(address):
    url='https://www.walletexplorer.com/address/'+address
    data= NetIO.readDataFrom(url)
    leading = 'part of wallet <a href="/wallet/'
    pattern=re.compile(r'part of wallet <a href="/wallet/[^>]+')
    match = re.search(pattern, data)
    addre = match.group()
    #print(addre)
    return addre[len(leading):-1]

# return a list of all wallet id of given type on "https://www.walletexplorer.com/"
def getAllWallet(Wtype="Exchanges"):
    url = "https://www.walletexplorer.com/"
    result = []

    data = NetIO.readDataFrom(url)
    # print(data)

    info = find_between(data, "<h3>" + Wtype, "</ul>")

    match = True
    pattern = re.compile(r'"/wallet/[^>]+')
    flag = 0
    while match:

        match = pattern.search(info, flag)
        if (match):
            result.append(match.group()[9:-1])
            # print(match.group())
            flag = int(match.span()[-1])


        else:
            break
    return result
