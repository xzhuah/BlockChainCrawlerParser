import urllib.request



def readDataFrom(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)  
  
    data = response.read()
    data = data.decode('utf-8')
    data=data.replace('\n','')
    return data

