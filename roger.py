#!/usr/bin/python

# requires a mailserver at localhost

import urllib.request
import urllib.error
import smtplib
import time
from email.mime.text import MIMEText

SOFTWARENAME = "Roger"
SOFTWAREVERSION = "0.1"
SOFTWAREDESCRIPTION = "HTTP status code monitoring"
USERAGENTSTRING = SOFTWARENAME + "/" + SOFTWAREVERSION + " (" + SOFTWAREDESCRIPTION + ")"

def monitor_status_code(testurl, initstatus, timeout):
    """Monitor status code of target until change

    Keyword arguments:
    testurl -- the target url
    initstatus -- the initial status code or error code for the target
    timeout -- number of minutes between tests
    """
    newstatus = 0
    status_changed = False

    while not status_changed:
        print("Entering test loop with timeout of", timeout, "minutes")
        time.sleep(timeout * 60)
        print("Testing...")
        try:
            connection = urllib.request.urlopen(
                urllib.request.Request(testurl, headers={'User-Agent': USERAGENTSTRING}), timeout=60)
            print("Statuscode", connection.getcode())
            if connection.getcode() != initstatus:
                newstatus = connection.getcode()
                print("New statuscode detected", initstatus, "->", newstatus)
                status_changed = True
            connection.close()
        except urllib.error.HTTPError as error:
            print(type(error), error)
            if error.code != initstatus:
                newstatus = error.getcode()
                print("New statuscode detected", initstatus, "->", newstatus)
                status_changed = True
    return newstatus

def roger(testurl, sender, receiver, timeout):
    """Monitor target for changes in status code and sent email notifications

    testurl -- the url of the target
    sender -- email adress that will be listed as sender of alert emails
    receiver -- email adress that will receive the alert emails
    timeout -- number of minutes between tests
    """
    initstatus = 0
    print(USERAGENTSTRING)
    print("Status monitoring for", testurl)

    # first time connecting to target to get initstatus
    try:
        print("Connecting...")
        connection = urllib.request.urlopen(
            urllib.request.Request(testurl, headers={'User-Agent': USERAGENTSTRING}), timeout=60)
        initstatus = connection.getcode()
        print("Initial statuscode", initstatus)
        connection.close()
    except urllib.error.HTTPError as error:
        print(type(error), error)
        initstatus = error.code
        print("Initial statuscode", initstatus)

    while True:
        newstatus = monitor_status_code(testurl, initstatus, timeout)
        mail_alert(testurl, sender, receiver, initstatus, newstatus)
        initstatus = newstatus

def send_with_local_mailserver(msg):
    """Send msg with mail server on localhost"""
    try:
        server = smtplib.SMTP('localhost')
        server.send_message(msg)
        server.quit()
        print("Alert sent")
        return True
    except Exception as exception:
        print(type(exception), exception)
        return False

def send_with_gmail_mailserver(msg):
    """Send msg with gmail mail server"""
    accountname = ""
    password = ""
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(accountname, password)
        server.sendmail(accountname, accountname, msg.as_string())
        server.quit()
        print("Alert sent")
        return True
    except Exception as exception:
        print(type(exception), exception)
        return False

def mail_alert(testurl, sender, receiver, initstatus, newstatus):
    """Create and send mail alert"""

    print("Composing alert email.")
    message = "Status of " + testurl + " changed from " + str(initstatus) + " to " + str(newstatus)
    msg = MIMEText(message)
    msg["Subject"] = "[" + SOFTWARENAME + "]" + " Status change for " + testurl
    msg["From"] = sender
    msg["To"] = receiver
    return send_with_local_mailserver(msg) # alternative: send_with_gmail(msg)
