import urllib2 
import time

domain = 'http://www.rolfny.com'
loadspeed = ''
try:
    stream = urllib2.urlopen(domain)
    start_time = time.time()
    out =stream.read()
    end_time = time.time()
    #time.sleep(10)
    out =stream.close()
    loadspeed= str(end_time-start_time)
    print(loadspeed)
except Exception as e:
    ipaddress="unknown"
    print(e)

