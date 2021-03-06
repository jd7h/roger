# roger
HTTP Status Code monitoring with notifications via email

## Usage and output
The tool takes the following input:

* testurl: the url to monitor
* sender: the email address that will be listed as the notification sender
* receiver: the email address where you want to receive the notification
* timeout: the interval (in minutes) for testing the HTTP status code

```
$ python
>>> import roger
>>> testurl = "http://github.com/jd7h/roger/master/README.md"
>>> sender = "sender@mymailserver.com"
>>> receiver = "receiver@mymailserver.com"
>>> timeout = 5
>>> roger.main(testurl,sender,receiver,timeout)
Roger/0.1 (HTTP status code monitoring)
Status monitoring for http://github.com/jd7h/roger/master/README.md
Connecting...
Initial statuscode 404
Entering test loop with timeout of 5 minutes
Testing...
New statuscode detected 404 -> 200
Composing alert email.
Finished
```
You will receive a notification email at receiver@mymailserver.com of the form:

```
Subject: [Roger] Status change for http://github.com/jd7h/roger/master/README.md
From: sender@mymailserver.com
To: receiver@mymailserver.com

Status of http://github.com/jd7h/roger/master/README.md changed from 404 to 200
```

## Ideas for improving this tool

* Check for the existence of a mail server
