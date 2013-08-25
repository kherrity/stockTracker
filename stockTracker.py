#!/usr/bin/env python

import sys, getopt
import urllib
import urllib2
import time
import datetime
from pytz import timezone

stopLoop = 0  ## controls the main loop

def sendText(number, message):
    texturl = 'http://www.onlinetextmessage.com/send.php'
    prov = '41'
    values = {'code' : '',
        'number' : number,
        'from' : 'k@junk.com',
        'remember' : 'n',
        'subject' : 'Stocks',
        'carrier' : prov,
        'quicktext' : '',
        'message' : message,
        's' : 'Send Message'}

    print "Sending text to: " + number
    data = urllib.urlencode(values)  ##text sender
    req = urllib2.Request(texturl, data)
    response = urllib2.urlopen(req)
    the_page = response.read() 

def isMarketClosed():
    marketClosed = False
    nyse = timezone('US/Eastern')
    est_time = datetime.datetime.now(nyse)
    #print est_time.strftime("%a, %d %b %Y %X")
    if 4 < est_time.weekday() < 7:
        marketClosed = True
    elif est_time.hour < 9 or est_time.hour > 16:
        marketClosed = True
    elif est_time.hour == 9 and est_time.minute < 30:
        marketClosed = True
    
    return marketClosed

def getEstTime():
    nyse = timezone('US/Eastern')
    est_time = datetime.datetime.now(nyse)
    #print est_time.strftime("%a, %d %b %Y %X")
    return est_time

def stop():
    global stopLoop
    stopLoop = 1

def main(argv):
    global stopLoop
    stopLoop = 0
    number = ''
    pThres = ''
    stocks = ''

    print "stopLoop: %d" % stopLoop

    try:
        opts, args = getopt.getopt(argv[1:], "hs:n:p:")
    except getopt.GetoptError:
        print argv[0] + ' -s <ticker symbol(s)> -n <phone #> -p <percent increase>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print argv[0] + ' -s <ticker symbol(s)> -n <phone #> -p <percent increase>'
            sys.exit()
        elif opt == '-s':
            stocks = arg.replace(' ',',').split(',') ## eliminate whitespace
            print stocks
            stocks = filter(None, stocks)
        elif opt == '-p':
            if arg:
                pThres = float(arg)
            else:
                print 'Invalid option.\n'
                sys.exit(2)
        elif opt == '-n':
            number = arg
        else:
            print 'Invalid option. \nUsage: ' + argv[0] + ' -s <ticker symbol(s)> -n <phone #> -p <percent increase>'
            sys.exit(2)

    if number == '' or pThres == '' or stocks == '':
        print 'Usage: ' + argv[0] + ' -s <ticker symbol(s)> -n <phone #> -p <percent increase>'
        sys.exit(2)

    sgn = 1
    loopPeriod = 10 #1 hour period
    marketCloseReported = False

    D = {}
    for s in stocks:
        D[s] = 0

    while not stopLoop:
        # Is the NYSE open?
#        if isMarketClosed():
#            if not marketCloseReported:
#                print "Market closed..."
#                marketCloseReported = True
#            time.sleep(600) # sleep 10 min
#            continue
#        else:
#            marketCloseReported = False
#            est_time = getEstTime()
#            if est_time.hour <= 10:
#                print "MARKET OPEN!"
       
        message = ''
        for stock in stocks:
            url = 'http://finance.yahoo.com/q?s=' + stock
            html_content = urllib2.urlopen(url).read()

            # get third arrow (which represents the stock price)
            narrow = 0
            idx = 0
            while narrow < 3:
                idx = html_content.find('_arrow', idx+1)
                narrow += 1

            if idx != -1:
                s = html_content[idx:idx+100]
                # determine direction of arrow (i.e. up or down)
                alt = s.find('alt=')
                lq = s.find('"', alt)
                rq = s.find('"', lq+1)
                upOrDown = s[lq+1:rq]
                if upOrDown == 'Down':
                    sgn = -1

                # get percentage change
                lparen = s.find('(')
                rparen = s.find(')')
                #print s[lparen+1:rparen]
                p = sgn * float(s[lparen+1:rparen-1])
                if p > pThres and p > D[stock]:
                    D[stock] = p
                    message += '| ' + stock.upper() + \
                      " has increased by " + str(p) + "% |"
                else:
                    print stock.upper() + " percent change (%.2f) not bigger than threshold (%.2f)" % (p, pThres)

        if message:
            print message
            #sendText(number, message) ## send sms text message
        # loop delay
        print "sleeping for " + str(loopPeriod) + " seconds"
        if stopLoop:
            break
        time.sleep(loopPeriod)

if __name__ == "__main__":
    main(sys.argv)
