# stayUpdated
fetch latest updates from http://aitplacements.com/ and receive updates through mobile SMS and desktop notification

## Installation

 1. Clone or fork the repo : git clone https://github.com/msdeep14/stayUpdated.git
 2. Edit username, password, mobile number, app key, app secret in main.py
 3. Set delay time according to your need (current delay = 5sec)
 4. Execute main.py from any of the directory(sinchSMS or way2SMS).

## Requirements
  1. python 2.7
  2. lxml
  3. requests
  4. sched
  5. cookielib, urllib
  6. sinchsms : get app_key and app_secret by registering app at [https://www.sinch.com/](https://www.sinch.com/)
  7. notify2
  
  There is no extra dependency for sending SMS through way2sms, you just need to register on way2sms portal.

