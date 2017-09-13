import urllib, urllib2, cookielib
import requests
from lxml import html
import time
from time import sleep
from sinchsms import SinchSMS
import sched

# set your credentials
username = 'your_username'
password = 'your_password'
number = 'your_mobile_number'
app_key = 'your_app_key'
app_secret = 'your_app_secret'
titlelist = []
# update time in seconds
delay = 5

s = sched.scheduler(time.time, time.sleep)

def sendSMS(inset):
    # extract message from set
    message = 'updates on aitplacements.com'
    i = 1
    for e in inset:
        news = str(e.encode('utf-8'))
        message = message + "\n"+str(i)+". "+ news
        i = i + 1
    # print message
    client = SinchSMS(app_key, app_secret)
    print("Sending '%s' to %s" % (message, number))

    response = client.send_message(number, message)
    message_id = response['messageId']
    response = client.check_status(message_id)

    while response['status'] != 'Successful':
        print(response['status'])
        time.sleep(1)
        response = client.check_status(message_id)

    print(response['status'])
    global titlelist
    titlelist = list(inset)
    # print titlelist

def checkForUpdate(mylist):
    # compare with mylist
    s1 = set(mylist)
    s2 = set(titlelist)
    # print mylist
    # print titlelist
    s3 = s1.union(s2) - s1.intersection(s2)
    if len(s3) is not 0:
        sendSMS(s3)
    else:
        print "no updates recently!"

def loginToWebsite(sc):
    print "checking for updates "
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    login_data = urllib.urlencode({'log' : username, 'pwd' :password})
    opener.open('http://aitplacements.com/wp-login.php', login_data)
    resp = opener.open('http://aitplacements.com/news/')
    # print resp.read()
    doc = html.fromstring(resp.read())
    # print html.tostring(doc1, pretty_print=True)
    raw_title = doc.xpath('//h1[@class="entry-title"]/a/text()')
    # print raw_title
    checkForUpdate(raw_title)
    s.enter(delay, 1, loginToWebsite, (sc,))


if __name__ == "__main__":
    s.enter(delay, 1, loginToWebsite, (s,))
    s.run()
