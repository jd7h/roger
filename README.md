# roger
HTTP Status Code monitoring with notifications via email

## Ideas for improving this tool

* Option for continuous monitoring
* Better and robuster error handling
* Check for the (existence) of a mail server

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
>>> sender = "someemail@mymailserver.com"
>>> reciever = "someotheremail@mymailserver.com"
>>> timeout = 5
>>> roger.main(testurl,sender,receiver,timeout)
Roger/0.1 (HTTP status code monitoring)
Status monitoring for http://github.com/jd7h/roger/master/README.md
Connecting...
Initial statuscode 404
Entering test loop with timeout of 5 minutes
Testing...
<class 'urllib.error.HTTPError'> HTTP Error 404: Not Found
New statuscode detected 200 -> 404
Composing alert email.
Finished
```
