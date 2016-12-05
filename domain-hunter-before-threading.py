from imports import *
from model import *

class DomainInfo():
    def __init__(self,domain):
        self.domain = domain
        self.estibotvalue = ''
        self.status = ''
        self.expirationdate = '2000/01/01'
        self.backordered = ''
        if self.checkNic():
            self.checkEstibot()

    def buildHtml(url):
        pass

    def checkNic(self):
        counter = 0
        max_attempts = 8
        while counter < max_attempts:
            try:
                url = 'https://www.nic.io/cgi-bin/whois?DOMAIN=' + self.domain + '.io'
                # url = 'https://www.nic.io/cgi-bin/whois?DOMAIN=' + 'jesus' + '.io'
                proxies = {
                    'http': 'http://{0}:{1}@62.212.82.72:6185'.format(proxyUser,proxyPass),
                    'https': 'http://{0}:{1}@62.212.82.72:6185'.format(proxyUser,proxyPass),
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
        max_attempts = 8
        while counter < max_attempts:
            try:
                url = 'http://www.estibot.com/appraise.php?a=appraise&data=' + self.domain + '.io'
                # url = 'http://www.estibot.com/appraise.php?a=appraise&data=' + 'jesus' + '.io'
                proxies = {
                    'http': 'http://{0}:{1}@62.212.82.72:6185'.format(proxyUser,proxyPass),
                    'https': 'http://{0}:{1}@62.212.82.72:6185'.format(proxyUser,proxyPass),
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
    try:
        option = getArg(sys.argv[1:])
        if option == "first":
            for domainRow in session.query(Domains).filter(Domains.expirationdate == None):
                print('Working on: ', domainRow.domain)
                domainInfo = DomainInfo(domainRow.domain)
                # currentDomainSession = session.query(Domains).filter_by(domain=domainRow.domain).first()
                # session.execute(update(main, values={main.domainRow.status: domainInfo.status}))
                domainRow.status = domainInfo.status
                domainRow.backordered = domainInfo.backordered
                domainRow.expirationdate = domainInfo.expirationdate
                domainRow.estibotvalue = domainInfo.estibotvalue
                print(domainInfo.status, domainInfo.backordered, domainInfo.expirationdate, domainInfo.estibotvalue)
            session.commit()
    except KeyboardInterrupt:
        session.commit()
        print('Manual stop')
        sys.exit()
