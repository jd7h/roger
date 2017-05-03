#!/usr/bin/python

# requires a mailserver at localhost

import urllib.request
import urllib.error
import smtplib
import time
from email.mime.text import MIMEText

def main(testurl,sender,receiver,timeout):
    softwarename = "Roger"
    softwareversion = "0.1"
    softwaredescription = "HTTP status code monitoring"
    useragentstring = softwarename + "/" + softwareversion + " (" + softwaredescription + ")"

    initstatus = 0
    newstatus = 0
    status_changed = False
    print(useragentstring)
    print("Status monitoring for",testurl)
    try:
        print("Connecting...")
        connection = urllib.request.urlopen(urllib.request.Request(testurl, headers= {'User-Agent': useragentstring}), timeout=60)
        initstatus = connection.getcode()
        print("Initial statuscode",initstatus)
        connection.close()
    except urllib.error.HTTPError as error:
        print(type(error),error)
        initstatus = error.code
        print("Initial statuscode",initstatus)
    while not status_changed:
        print("Entering test loop with timeout of",timeout,"minutes")
        time.sleep(timeout * 60)
        print("Testing...")
        try:
            connection = urllib.request.urlopen(urllib.request.Request(testurl, headers = {'User-Agent': useragentstring}), timeout=60)
            print("Statuscode",connection.getcode())
            if connection.getcode() != initstatus:
                newstatus = connection.getcode()
                print("New statuscode detected",initstatus,"->",newstatus)
                status_changed = True
            connection.close()
        except urllib.error.HTTPError as error:
            print(type(error),error)
            if error.code != initstatus:
                newstatus = error.getcode()
                print("New statuscode detected",initstatus,"->",newstatus)
                status_changed = True

    # time for an alert
    print("Composing alert email.")
    message = "Status of " + testurl + " changed from " + str(initstatus) + " to " + str(newstatus)
    msg = MIMEText(message)
    msg["Subject"] = "[" + softwarename + "]" + " Status change for " + testurl 
    msg["From"] = sender
    msg["To"] = receiver
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
    print("Finished")
