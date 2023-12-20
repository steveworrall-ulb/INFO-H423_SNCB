from urllib.request import urlopen
import time

def ele_get(listRecords):
    coordinates = ''
    idList = []
    for x in listRecords:
        coordinates += x[1] + ',' + x[2] + "|"
        idList.append(x[0])
    coordinates = coordinates[:-1]
    eleList = []
    if len(coordinates) > 5:
        with urlopen("http://ubuntuvm:5000/v1/etopo1?locations=" + coordinates) as response:
            body = response.read().decode("utf-8")

        while body.find('elevation') != -1:
            start = body.find('elevation') + 12
            body = body[start:]
            end = body.find(',')
            eleList.append(body[:end])
            body = body[end:]




    returnList = []
    if len(idList) == len(eleList):
        i=0
        for x in idList:
            returnList.append([x, eleList[i]])
            i += 1
    else:
        raise ValueError('error returning values from API - record size mismatch')
    return returnList

def write_to_file(OutList):
    #write to file...
    OutputString = ''
    for x in OutList:
        OutputString += (x[0] + ";" + x[1] + "\n")


    f = open('elevation_etopo1.csv',"a")            #open for overwrite - w (note - a is for append)
    f.write(OutputString)
    f.close()
    print("writing - elevation_etopo1.csv")

def open_file():
    #f = open('ar41_for_ulb_mini.csv')              #open the file
    f = open('ar41_for_ulb.csv')                    #open the file
    myList = []
    i = 0
    for l in f.readlines():                         #extract lines l from file
        if i != 0:                                  #exclude line 0
            l = l.strip().upper()
            id = l.split(';')[0]
            lat = l.split(';')[3]
            long = l.split(';')[4]
            myList.append([id, lat, long])
        i+=1
        if i % 500 == 0:
            OutList = ele_get(myList)
            write_to_file(OutList)
            myList = []
            time.sleep(.5)
            # if i % 5000 == 0:
            #     return
    #write remaining entries
    OutList = ele_get(myList)
    write_to_file(OutList)


open_file()
print('job complete...')