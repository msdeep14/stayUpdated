import urllib, urllib2, cookielib
import requests
from lxml import html
import time
from time import sleep
import sched
import notify2

# set your credentials
# username is mobile number
# registered on way2sms
username = 'way2smsUsername'
password = 'way2smsPassword'

# credentials for aitplacements.com
AITusername = 'AITusername'
AITpassword = 'AITpassword'

# update time in seconds
delay = 5

# add mobile numbers to this list to whom
# you want to send SMS
numberlist = ['7798xxxxxx']

# global list for storing updates
titlelist = []

s = sched.scheduler(time.time, time.sleep)


# send desktop notification in case of any update
def desktopNotify(message2):
    print("sending desktop Notification")
    notify2.init("updateNotifier")

    n = notify2.Notification('Updates from aitplacements.com',message2)
    n.show()
    time.sleep(3)


# send SMS in case of any update
def sendSMS(message2, inset):
    for number in numberlist:
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        # way2sms limitations:
        # 140 chars per msg
        # 100 free msgs per day
        login_data = 'username=' + username + '&password=' + password + '&Submit=Sign+in'
        opener.open('http://site24.way2sms.com/Login1.action?', login_data)

        print("sending SMS to " + number)
        session_id =str(cj).split('~')[1].split(' ')[0]
        smsUrl = 'http://site24.way2sms.com/smstoss.action?'
        smsData = 'ssaction=ss&Token=' + session_id + '&mobile=' + number + '&message=' + message2 + '&msgLen=136'
        opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token=' + session_id)]
        try:
            smsPage = opener.open(smsUrl, smsData)
            # doc = html.fromstring(smsPage.read())
            # print html.tostring(doc, pretty_print=True)
        except IOError:
            print ("SMS sending failed!")

    global titlelist
    titlelist = list(inset)
    # print titlelist

# check for new updates
def checkForUpdate(mylist):
    # get difference in mylist and
    # titlelist for updates
    s = set(titlelist)
    temp3 = [x for x in mylist if x not in s]
    if len(temp3) is not 0:
        # convert it into string message
        inlist = list(temp3)
        message2 = ''
        inlistLen = len(inlist)
        for i in range(2):
            if i < inlistLen:
                message2 = message2 + '\n' + str(inlist[i].encode('utf-8'))
        # send updates to mobile and desktop
        sendSMS(message2, temp3)
        desktopNotify(message2)
    else:
        print ("no updates recently!")


# login to aitplacements.com
def loginToWebsite(sc):
    print ("checking for updates ")
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    login_data = urllib.urlencode({'log' : AITusername, 'pwd' :AITpassword})
    opener.open('http://aitplacements.com/wp-login.php', login_data)
    resp = opener.open('http://aitplacements.com/news/')
    # print (resp.read())
    doc = html.fromstring(resp.read())
    # print (html.tostring(doc, pretty_print=True))
    raw_title = doc.xpath('//h1[@class="entry-title"]/a/text()')
    # print (raw_title)
    checkForUpdate(raw_title)
    s.enter(delay, 1, loginToWebsite, (sc,))


if __name__ == "__main__":
    s.enter(delay, 1, loginToWebsite, (s,))
    s.run()
