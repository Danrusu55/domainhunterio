from imports import *
from model import *

class startThread (threading.Thread):
    def __init__(self, rowStart, rowEnd):
        threading.Thread.__init__(self)
        self.rowStart = rowStart
        self.rowEnd = rowEnd
        self.sql = "UPDATE main SET `status`='{0}', `backordered`='{1}', `expirationdate`='{2}', `estibotvalue`='{3}' where `domain`='{4}'"
    def run(self):
        try:
            conn = MySQLdb.connect(host=host,user=mySqlUser,passwd=mySqlPass,db=dbName)
            cur = conn.cursor()
            cur.execute("SELECT * FROM main where `status` is NULL AND `number` > {0} and `number` < {1};".format(self.rowStart,self.rowEnd))
            domainRows = cur.fetchall()
            for domainRow in domainRows:
                domainInfo = DomainInfo(domainRow[1])
                print(domainRow[1],domainInfo.status, domainInfo.backordered, domainInfo.expirationdate, domainInfo.estibotvalue)
                if domainInfo.expirationdate:
                    cur.execute(self.sql.format(domainInfo.status, domainInfo.backordered, domainInfo.expirationdate, domainInfo.estibotvalue, domainInfo.domain))
                else:
                    cur.execute("UPDATE main SET `status`='{0}' where `domain`='{1}'".format(domainInfo.status,domainInfo.domain))
                conn.commit()

            # some_session.commit()
        except KeyboardInterrupt:
            #Session.commit()
            print('Manual stop')
            sys.exit()
        finally:
            if conn:
                conn.close()

class DomainInfo():
    def __init__(self,domain):
        self.domain = domain
        self.estibotvalue = ''
        self.status = ''
        self.expirationdate = ''
        self.backordered = ''
        if self.checkNic():
            self.checkEstibot()

    def buildHtml(url):
        pass

    def checkNic(self):
        counter = 0
        max_attempts = 15
        while counter < max_attempts:
            try:
                url = 'https://www.nic.io/cgi-bin/whois?DOMAIN=' + self.domain + '.io'
                # url = 'https://www.nic.io/cgi-bin/whois?DOMAIN=' + 'jesus' + '.io'
                proxies = {
                    'http': 'http://{0}:{1}@{2}:{3}'.format(proxyUser,proxyPass,proxyIP,proxyPort),
                    'https': 'https://{0}:{1}@{2}:{3}'.format(proxyUser,proxyPass,proxyIP,proxyPort),
                }
                content = requests.get(url,proxies=proxies,headers={'User-Agent': 'Mozilla/5.0'}).content
                soup = BeautifulSoup(content,"html.parser")
                # STATUS
                self.status = soup(text=re.compile(r'Domain Status :'))[0].parent.parent.find_all('td')[1].get_text()
                # print(self.status)
                if 'Reserved' in self.status:
                    return False
                else:
                    # EXPIRATION DATE
                    self.expirationdate = soup(text=re.compile(r'Redemption'))[0].parent.parent.get_text()[0:10]
                    # print(self.expirationdate)

                    # BACKORDERED?
                    self.backordered = soup(text=re.compile(r'What is a back-order?'))[0].parent.parent.get_text()
                    if "Already" in self.backordered:
                        self.backordered = "Already backordered"
                    else:
                        self.backordered = "Available"
                    # print(self.backordered)
                    return True
            except Exception as err:
                # print('Failed checkNic: ', err)
                counter += 1

    def checkEstibot(self):
        counter = 0
        max_attempts = 15
        while counter < max_attempts:
            try:
                url = 'http://www.estibot.com/appraise.php?a=appraise&data=' + self.domain + '.io'
                # url = 'http://www.estibot.com/appraise.php?a=appraise&data=' + 'jesus' + '.io'
                proxies = {
                    'http': 'http://{0}:{1}@{2}:{3}'.format(proxyUser,proxyPass,proxyIP,proxyPort),
                    'https': 'https://{0}:{1}@{2}:{3}'.format(proxyUser,proxyPass,proxyIP,proxyPort),
                }
                content = requests.get(url,proxies=proxies,headers={'User-Agent': 'Mozilla/5.0'}).content
                soup = BeautifulSoup(content,"html.parser")

                # ESTIBOT VALUE
                self.estibotvalue = soup.find(id='td_value').get_text()
                # print(self.estibotvalue)
                return True
            except Exception as err:
                # print('Failed checkEstibot: ', err)
                counter += 1


def getArg(argv):
    option = ''
    try:
        opts, args = getopt.getopt(argv,'hr:')
    except getopt.GetoptError:
        print 'domain-hunter.py -r <first,continual>'
        sys.exit(2)
    if not opts:
        print("-r not given. domain-hunter.py -r <first,continual>")
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print 'domain-hunter.py -r <first,continual>'
            sys.exit()
        elif opt in "-r":
            option = arg
    return option

if __name__ == "__main__":
    # global

    ToCommitDictionary = {}

    try:
        option = getArg(sys.argv[1:])
        if option == "first":
            numRows = len(some_session.query(Domains).all())
            threadsToUse = 15
            rowsPer = numRows / threadsToUse
            threads = []

            for i in range(1,numRows,rowsPer):
                thread = startThread(i, i + rowsPer)
                thread.daemon = True
                thread.start()
                threads.append(thread)
            while True:
                time.sleep(1)
            # for t in threads:
                # t.join()
                '''
            # to run just one
            conn = MySQLdb.connect(host=host,user=mySqlUser,passwd=mySqlPass,db=dbName)
            cur = conn.cursor()
            cur.execute("SELECT * FROM main where `status` is NULL")
            domainRows = cur.fetchall()
            sql = "UPDATE main SET `status`='{0}', `backordered`='{1}', `expirationdate`='{2}', `estibotvalue`='{3}' where `domain`='{4}'"
            for domainRow in domainRows:
                domainInfo = DomainInfo(domainRow[1])
                if domainInfo.status:
                    print(domainInfo.domain,domainInfo.status, domainInfo.backordered, domainInfo.expirationdate, domainInfo.estibotvalue)
                    if domainInfo.expirationdate:
                        cur.execute(sql.format(domainInfo.status, domainInfo.backordered, domainInfo.expirationdate, domainInfo.estibotvalue, domainInfo.domain))
                    else:
                        cur.execute("UPDATE main SET `status`='{0}' where `domain`='{1}'".format(domainInfo.status,domainInfo.domain))
                    conn.commit()
                '''
    except KeyboardInterrupt:
        # session.commit()
        print('Manual stop main')
        sys.exit()
    except Exception as err:
        print('error: ', err)
        sys.exit()
    finally:
        if conn:
            conn.close()
