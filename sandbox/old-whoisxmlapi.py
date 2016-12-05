import urllib2
import json,threading
import xml.etree.ElementTree as etree

class startThread (threading.Thread):
    def __init__(self, threadID, name, domain):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.domain = domain
    def run(self):
        getExpiryDate(self.domain)

def getExpiryDate(domain):
    # VARIABLES
    format = "XML"
    username = "daniel7rusu"
    password = "$Krys1212"

    url = 'http://www.whoisxmlapi.com/whoisserver/WhoisService?domainName=' + domain + '&username=' + username + '&password=' + password + '&outputFormat=' + format
    result = etree.parse(urllib2.urlopen(url))
    root = result.getroot()

    # A function to recursively build a dict out of an ElementTree
    def etree_to_dict(t):
        if (len(list(t)) == 0):
            d = t.text
        else:
            d = {}
            for node in list(t):
                d[node.tag] = etree_to_dict(node)
                if isinstance(d[node.tag], dict):
                    d[node.tag] = d[node.tag];
        return d

    # Create the dict with the above function.
    result = {root.tag :etree_to_dict(root)}

    # Get a few data members.
    try:
        if 'expiresDate' in result['WhoisRecord']['registryData'].keys():
            expiresDate = result['WhoisRecord']['registryData']['expiresDate']
            print(domain,", ",expiresDate)
            with open('/Users/danrusu/code/domain-hunter-com/domains-out.txt','a') as outFile:
                outFile.write('\n' + domain + ', ' + expiresDate)
        else:
            pass
    except Exception as err:
        print(err)

# MAIN
if __name__ == "__main__":
    # VARIABLES
    format = "XML"
    username = "daniel7rusu"
    password = "$Krys1212"
    domainsArray = []
    # put all domains into an array

    with open('/Users/danrusu/code/domain-hunter-com/domains.txt') as inFile:
        for line in inFile:
            domain = line.replace('\n','') +'.io'
            domainsArray.append(domain)

    #split up and start multithread with the array
    campaignsPerChunk = 20
    campaignChunks = [domainsArray[x:x+campaignsPerChunk] for x in range(0, len(domainsArray), campaignsPerChunk)]
    for idx,campaignChunk in enumerate(campaignChunks):
        print(campaignChunk[0])
        print('Working on chunk {0} out of {1}'.format(idx,len(campaignChunks)))
        threads = []
        numOfThreads = len(campaignChunk)
        if numOfThreads < 0:
            break
        else:
            thread1 = startThread(1, "Thread-1",campaignChunk[0])
            thread2 = startThread(2, "Thread-2",campaignChunk[1])
            thread3 = startThread(3, "Thread-3",campaignChunk[2])
            thread4 = startThread(4, "Thread-4",campaignChunk[3])
            thread5 = startThread(5, "thread-5",campaignChunk[4])
            thread6 = startThread(6, "Thread-6",campaignChunk[5])
            thread7 = startThread(7, "Thread-7",campaignChunk[6])
            thread8 = startThread(8, "thread-8",campaignChunk[7])
            thread9 = startThread(9, "thread-9",campaignChunk[8])
            thread10 = startThread(10, "Thread-10",campaignChunk[9])
            thread11 = startThread(11, "Thread-11",campaignChunk[10])
            thread12 = startThread(12, "Thread-12",campaignChunk[11])
            thread13 = startThread(13, "Thread-13",campaignChunk[12])
            thread14 = startThread(14, "Thread-14",campaignChunk[13])
            thread15 = startThread(15, "thread-15",campaignChunk[14])
            thread16 = startThread(16, "Thread-16",campaignChunk[15])
            thread17 = startThread(17, "Thread-17",campaignChunk[16])
            thread18 = startThread(18, "thread-18",campaignChunk[17])
            thread19 = startThread(19, "thread-19",campaignChunk[18])
            thread20 = startThread(20, "Thread-20",campaignChunk[19])
            thread1.start()
            thread2.start()
            thread3.start()
            thread4.start()
            thread5.start()
            thread6.start()
            thread7.start()
            thread8.start()
            thread9.start()
            thread10.start()
            thread11.start()
            thread12.start()
            thread13.start()
            thread14.start()
            thread15.start()
            thread16.start()
            thread17.start()
            thread18.start()
            thread19.start()
            thread20.start()
            threads.append(thread1)
            threads.append(thread2)
            threads.append(thread3)
            threads.append(thread4)
            threads.append(thread5)
            threads.append(thread6)
            threads.append(thread7)
            threads.append(thread8)
            threads.append(thread9)
            threads.append(thread10)
            threads.append(thread11)
            threads.append(thread12)
            threads.append(thread13)
            threads.append(thread14)
            threads.append(thread15)
            threads.append(thread16)
            threads.append(thread17)
            threads.append(thread18)
            threads.append(thread19)
            threads.append(thread20)
            for t in threads:
                t.join()
        #break
