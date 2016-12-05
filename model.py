from imports import *

mySqlUser = os.environ['MYSQL_USER']
mySqlPass = os.environ['MYSQL_PASS']
host = '127.0.0.1'
dbName = 'DomainHunterDB'

engine = create_engine('mysql+mysqldb://{0}:{1}@{2}:3306/{3}'.format(mySqlUser,mySqlPass,host,dbName), echo=False, pool_size=60, max_overflow=100)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
some_session = Session()

Base = declarative_base()

'''
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
'''

class Domains(Base):
    __tablename__ = 'main'
    number = Column(Integer, primary_key=True)
    domain = Column(String(100))
    status = Column(String(100))
    expirationdate = Column(DateTime)
    estibotvalue = Column(String(30))
    backordered = Column(String(100))

    def __init__(self,domain,expirationdate,estibotvalue,backordered):
        # self.number = number
        self.domain = domain
        self.expirationdate = expirationdate
        self.estibotvalue = estibotvalue
        self.backordered = backordered

    def __repr__(self):
        return "<Domains(number='{0}',domain='{1}',expirationdate='{2}',estibotvalue='{3}',backordered='{4}')>".format(self.number,self.domain,self.expirationdate,self.estibotvalue,self.backordered)
