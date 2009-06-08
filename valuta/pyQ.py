#!/usr/bin/env python

##################################################
# Name:        pyQ - Python Quote Grabber
# Author:      Rimon Barr <barr@cs.cornell.edu>
# Start date:  10 January 2002
# Purpose:     Retrieve stock quote data in Python
# License:     GPL 2.0

##################################################
# Activity log:
#
# 10/01/02 - Initial release
# 14/10/02 - Yahoo changed url format
# 31/10/02 - More convenient programmatic interface and local caching
# 21/09/04 - Updated by Alberto Santini to accomodate Yahoo changes
# 27/01/05 - Updated by Alberto Santini to accomodate Yahoo changes
# 11/01/07 - Updated by Ehud Ben-Reuven, Historical currency exchnage tickers
#            (e.g. USDEUR=X) are retrieved from www.oanda.com
# 15/03/07 - code cleanup; updated Yahoo date format, thanks to Cade Cairns

import os, sys, re, traceback, getopt, urllib, string, anydbm, time

Y2KCUTOFF=60
__version__ = "0.7"
CACHE='stocks.db'
DEBUG = 1

def showVersion():
  print 'pyQ v%s, by Rimon Barr:' % __version__
  print '- Python Yahoo Quote fetching utility'

def showUsage():
  print
  showVersion()
  print '''
Usage: pyQ [-i] [start_date [end_date]] ticker [ticker...]
       pyQ -h | -v

  -h, -?, --help      display this help information
  -v, --version       display version'
  -i, --stdin         tickers fed on stdin, one per line

  - date formats are yyyymmdd
  - if enddate is omitted, it is assume to be the same as startdate
  - if startdate is omitted, we use *current* stock tables and otherwise, use
    historical stock tables. Current stock tables will give previous close
    price before market closing time.)
  - tickers are exactly what you would type at finance.yahoo.com
  - output format: "ticker, date (yyyymmdd), open, high, low, close, vol"
  - currency exchange rates are also available, but only historically.
    The yahoo ticker for an exchange rate is of the format USDEUR=X. The
    output format is "ticker, date, exchange".

  Send comments, suggestions and bug reports to <rimon@acm.org>
'''

def usageError():
  print "rimdu: command syntax error"
  print "Try `rimdu --help' for more information."

def isInt(i):
  try: int(i); return 1
  except: return 0

def splitLines(buf):
  def removeCarriage(s):
    if s[-1]=='\r': return s[:-1]
    else: return s
  return map(removeCarriage,filter(lambda x:x, string.split(buf, '\n')))

def parseDate(d):
  '''convert yyyymmdd string to tuple (yyyy, mm, dd)'''
  return (d[:-4], d[-4:-2], d[-2:])

def yy2yyyy(yy):
  global Y2KCUTOFF;
  yy=int(yy) % 100
  if yy<Y2KCUTOFF: return `yy+2000`
  else: return `yy+1900`

# convert month to number
MONTH2NUM = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
  'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
def dd_mmm_yy2yyyymmdd(d):
  global MONTH2NUM
  d=string.split(d, '-')
  day='%02d' % int(d[0])
  month='%02d' % MONTH2NUM[d[1]]
  year=yy2yyyy(d[2])
  return year+month+day

DAYSECS = 60 * 60 * 24
def allDates(d1,d2):
  '''Return all dates in ascending order. Inputs in yyyymmdd format'''
  if int(d1)>int(d2): raise IndexError, 'd1 must be smaller than d2'
  d1 = time.mktime(time.strptime(d1, '%Y%m%d'))
  d2 = time.mktime(time.strptime(d2, '%Y%m%d'))+1
  dates = []
  while d1 < d2:
    dates.append(time.strftime('%Y%m%d', time.localtime(d1)))
    d1 += DAYSECS
  return dates

def aggDates(dates):
  '''Aggregate list of dates (yyyymmdd) in range pairs'''
  if not dates: return []
  aggs = []
  dates=[int(date) for date in dates]
  dates.sort()
  high=dates.pop(0)
  low=high
  for date in dates:
    if date==high+1: high=date
    else:
      aggs.append( (low, high) )
      high=date; low=high
  aggs.append( (low, high) )
  return [(str(low),str(high)) for (low, high) in aggs]

def getRate(d1,d2,ticker):
  if not (len(ticker)==8 and ticker.endswith('=X')):
    raise Exception('Illegal FX rate ticker')
  cur1,cur2=ticker[0:3], ticker[3:6]
  def yyyymmdd2mmddyy(d): return d[4:6]+'%2F'+d[6:8]+'%2F'+d[2:4]
  def mmddyy2yyyymmdd(d):
    if len(d)!=10 or d[2]!='/' or d[5]!='/':
      raise Exception('Illegal date format')
    return d[6:10]+d[0:2]+d[3:5]
  d1,d2=yyyymmdd2mmddyy(d1),yyyymmdd2mmddyy(d2)
  url = 'http://www.oanda.com/convert/fxhistory'
  query = (
    ('lang','en'),
    ('date1',d1),
    ('date',d2),
    ('date_fmt','us'),
    ('exch',cur1),
    ('exch2',''),
    ('expr',cur2),
    ('expr2',''),
    ('margin_fixed','0'),
    ('SUBMIT','Get+Table'),
    ('format','CSV'),
    ('redirected','1')
    )
  query = map(lambda (var, val): '%s=%s' % (var, str(val)), query)
  query = string.join(query, '&')
  query1 = 'lang=en&date1=%s&date=%s&date_fmt=us&exch=%s&exch2=&expr=%s&expr2=&margin_fixed=0&&SUBMIT=Get+Table&format=CSV&redirected=1'%(d1,d2,cur1,cur2)
  page = urllib.urlopen(url+'?'+query).read().splitlines()
  table=False
  result=[]
  for l in page:
    if l.startswith('<PRE>'): table=True; l=l[5:]
    elif l.startswith('</PRE>'): table=False
    if table:
      l=string.split(l, ',')
      l[0]=mmddyy2yyyymmdd(l[0])
      l=[ticker]+l
      result.append(l)
  return result

def getTicker(d1, d2, ticker):
  if len(ticker)==8 and ticker.endswith('=X'): return getRate(d1,d2,ticker)
  if DEBUG: print '# Quering Yahoo!... for %s (%s-%s)' % (ticker, d1, d2)
  d1,d2=parseDate(d1),parseDate(d2)
  url='http://ichart.finance.yahoo.com/table.csv'
  query = (
    ('a', '%02d' % (int(d1[1])-1)),
    ('b', d1[2]),
    ('c', d1[0]),
    ('d', '%02d' % (int(d2[1])-1)),
    ('e', d2[2]),
    ('f', d2[0]),
    ('s', ticker),
    ('y', '0'),
    ('g', 'd'),
    ('ignore', '.csv'),)
  query = '&'.join(map(lambda (var, val): '%s=%s' % (var, str(val)), query))
  f=urllib.urlopen(url+'?'+query)
  lines=splitLines(f.read())
  if re.match('no prices', lines[0], re.I): return
  lines,result=lines[1:],[]
  for l in lines:
    l=l.split(',')
    result.append([ticker,l[0].replace('-','')]+l[1:])
  return result

def getCachedTicker(d1, d2, ticker, forcefailed=0):
  '''Get tickers, hopefully from cache.
    d1, d2 = yyyymmdd starting and ending
    ticker = symbol string
    forcefailed = integer for cachebehaviour
      =0 : do not retry failed data points
      >0 : retry failed data points n times
      -1 : retry failed data points, reset retry count
      -2 : ignore cache entirely, refresh ALL data points'''
  dates = allDates(d1, d2)
  # get from cache
  data = {}
  db = anydbm.open(CACHE, 'c')
  for d in dates:
    try: data[ (d, ticker) ] = db[ `(d, ticker)` ]
    except KeyError: pass
  # forced failed
  if forcefailed:
    for k in data.keys():
      if (forcefailed==-2 or
          (forcefailed==-1 and type(eval(data[k]))==type(0)) or
          eval(data[k]) < forcefailed):
        del data[k]
  # compute missing
  cached = [d for d,ticker in data.keys()]
  missing = [d for d in dates if d not in cached]
  for d1, d2 in aggDates(missing):
    try:
      tmp = getTicker(d1, d2, ticker)
      for t in tmp:
        _, d, datum = t[0], t[1], t[2:]
        data[ (d, ticker) ] = db[ `(d, ticker)` ] = `datum`
    except: pass
  # failed
  cached = [d for d,ticker in data.keys()]
  failed = [d for d in missing if d not in cached]
  for d in failed:
    try: times = eval(db[ `(d, ticker)` ])
    except: times = 0
    if forcefailed<0: times = 1
    if times < forcefailed: times = times + 1
    data [ (d, ticker) ] = db[ `(d, ticker)` ] = `times`
  # result
  result = []
  for d in dates:
    datum = eval(data[(d,ticker)])
    if type(datum) != type(0): result.append( [ticker, d] + datum )
  return result

def getTickers(d1, d2, tickers, forcefailed=0):
  '''Get tickers.
    d1, d2 = yyyymmdd starting and ending
    tickers = list of symbol strings
    forcefailed = integer for cachebehaviour
      =0 : do not retry failed data points
      >0 : retry failed data points n times
      -1 : retry failed data points, reset retry count
      -2 : ignore cache entirely, refresh ALL data points'''
  result = []
  for t in tickers: result += getCachedTicker(d1, d2, t, forcefailed)
  return result

def getTickersNowChunk(tickers):
  url='http://finance.yahoo.com/d/quotes.csv?%s' % urllib.urlencode(
      {'s':''.join(tickers), 'f':'sohgpv', 'e':'.csv'})
  f=urllib.urlopen(url)
  lines,t,result=splitLines(f.read()),time.localtime(),[]
  for l in lines:
    l=l.split(',')
    result.append([string.lower(l[0][1:-1]), '%4d%02d%02d'%t[0:3]]+l[1:])
  return result

def getTickersNow(tickers):
  result = []
  while tickers:
    result += getTickersNowChunk(tickers[:150])
    tickers = tickers[150:]
  return result

def main():
  # parse options
  try: opts, args = getopt.getopt(sys.argv[1:], 'hv?i', ['help', 'version', 'stdin'])
  except getopt.GetoptError: usageError(); return
  # process options
  stdin=0
  for o, a in opts:
    if o in ("-h", "--help", "-?"): showUsage(); return
    if o in ("-v", "--version"): showVersion(); return
    if o in ("-i", "--stdin"): stdin=1
  t=time.localtime()
  startdate='%4d%02d%02d' % (t[0], t[1], t[2])
  enddate=startdate
  today,tickers,argpos=1,[],-1
  for a in args:
    argpos=argpos+1
    if argpos==0 and isInt(a): startdate=enddate=a; today=0; continue
    if argpos==1 and isInt(a):
      enddate=a
      if a=='0': enddate='%4d%02d%02d' % (t[0], t[1], t[2])
      continue
    tickers+=[a]
  if stdin: tickers=tickers+splitLines(sys.stdin.read())
  if not len(tickers): showUsage(); return
  if today:
    result = getTickersNow(tickers)
    for l in result: print ','.join(l)
  else:
    result = getTickers(startdate, enddate, tickers)
    for l in result: print ','.join(l)

try: 
  if __name__=='__main__': main()
except KeyboardInterrupt: traceback.print_exc(); print 'Break!'


