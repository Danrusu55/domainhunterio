## Purpose

Attempt to find valuable domains to snipe 60-80 days before expiration date.

## Phases to project

1. Check using list of ~60k most common words + small character combinations. up to 11 characters?
2. Check full list of words and character combinations + common word combos? ex: orderbook. check if value in these..

## In and Out

In: list of word domains to check + list of 2 character combinations
Out:
  Sheet of:
    Expiration date
      1. nic.io - soup and proxies
      2. Whois cmd - Proxify whois query using proxify software on entire computer/in program somehow
    Estibot value
      1. soup on site.
  Script that will check the db I specify dates between to check for backorder available or not. Can eventually put this on heroku to message me.


## Testing

1. Proxies on the sites I need to soup
  Nic.io = good w/ proxy rack https proxies used
    on failure = times out
  Estibot = good w/ https proxies also. Just slow...
    on failure = shows please login


## Sudo

check it once for:
  estibotvalue
check it continually each month for:
  expirationdate - used to know which to check out in the future
  domain status
    Reserved
    live
    expired
  backordered or not
  looking for:
    status: expired
    backordered: no


class domainInfo(domain):
  checkNic():
    expirationDate = ''
    backorder = ''
    try 5 times:
      timeout after 10 seconds

  checkEstibot():
    estibot = ''
    try 5 times:
      if not 'Register today':
        grab value from page
      else value = fail
    return value



arg = onetime
  for domain in list (filter list with empty estibot)
    checkNic
    checkEstibot
arg = checkbackorder
  get the dates arg to get domains to do
    checkNic

query # of rows = 10000
threadsToUse = 25
rowsPer = 10000 / 25 = 400
1 - 400
401 - 800
801 - 1200

for i in range(1,10000,400)
  threadi = startThread(i,i+rowsPer)
thread1()
rowArray = split into # of threads
thread - with rowArray
  function query
    for domainRow in session.query(rowArray)
      call class & update
