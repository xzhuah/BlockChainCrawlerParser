#This program will provide a function that read all the local file and return a map <publicaddress,walletID> 

import os

from IOUtil import NetIO
from IOUtil import CsvIO

#return a haspmap for finding wallet of a public key
def getHashpub2wallet(hashdir):
    the_map = {}
    lst = os.listdir(hashdir)
    lst.sort()
    for file in lst:

        content = CsvIO.readFile(hashdir + "/" + file)
        content = content.split("\n")
        for line in content:
            #print(line,file.replace(".csv",""))
            the_map[line]=file.replace(".csv","") # this filename must be the wallet_id
        #print("finish ",file)
    return the_map

#return 3 list of object, pay for fee, sent to, receive from, transaction sorted by time
def classifyTransaction(Trandir,filename_proto=""):
    pay_for_fee=[]
    sent_to=[]
    receive_from=[]
    file_list = os.listdir(Trandir)
    if(filename_proto==""):
        filename_proto = str(file_list[0])[0:-5] #hardcode here since the file is produced by this program and will always end with num.csv, [0] will be 1.csv
    for file in range(1,len(file_list)+1):
        
        filename = Trandir+"/"+filename_proto+str(file)+".csv"
        #print(filename)
        content = CsvIO.readFile(filename).replace('"', '')
        content = content.split("\n")
        #content[0] block info
        #content[1] title
        try:
            for i in range(2,len(content)-1):
                info_list = content[i].split(",")
                #print(info_list,file,i)
                if(info_list[1]!=""):
                    # receive_from
                    amount = float(info_list[2])
                    if amount==0:
                        # the website provides information with some mistakes
                        continue
                    receive_from.append( {"time":info_list[0],"from":info_list[1],"amount":amount,"balance":float(info_list[5]),"transaction":info_list[6]} )
                elif (info_list[4]!="(fee)"):
                     # sent_to
                    amount = float(info_list[3])
                    if amount == 0:
                        continue
                    sent_to.append( {"time":info_list[0],"to":info_list[4],"amount":amount,"balance":float(info_list[5]),"transaction":info_list[6]} )

                else:
                    #pay_for_fee
                    pay_for_fee.append( {"time":info_list[0],"to":info_list[4],"amount":float(info_list[3]),"balance":float(info_list[5]),"transaction":info_list[6]} )

        except:
            continue
    return pay_for_fee , sent_to , receive_from


            
def __test():
    hashmap = getHashpub2wallet("testfile/public")
    key = "35DhRKpHoo3Ue4aHCVbTYhP1xPpwNbmtMR"
    key2 = "16EbtdyjrXqDUt3BEHngM9iftPZAGpB7fZ"
    if key in hashmap:

        print(hashmap[key])
    else:
        print("NONE")
    if key2 in hashmap:

        print(hashmap[key2])
    else:
        print("NONE")

    pay_for_fee, sent_to, receive_from = classifyTransaction("testfile/bitstamp")
    print(len(pay_for_fee), len(sent_to), len(receive_from))
    print(pay_for_fee[0], sent_to[0], receive_from[0])

    pay_for_fee, sent_to, receive_from = classifyTransaction("testfile/Btc38.com2016-12-16To2017-10-29")
    print(len(pay_for_fee), len(sent_to), len(receive_from))
    print(pay_for_fee[0], sent_to[0], receive_from[0])

#__test()
