# write content to a localfile filename
def writeToFile(filename, content):
    f = open(filename, 'w')
    f.write(content)
    f.close()


def appendToFile(filename, content):
    f = open(filename, 'a')
    f.write(content + '\n')
    f.close()


def readFile(filename):
    file = open(filename, "r")
    content = file.read()
    file.close()
    return content