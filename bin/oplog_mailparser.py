#!/usr/bin/env python
# version: 2.0.0
# http://docs.python.org/library/email.message.html
# http://docs.python.org/library/email-examples.html
import sys, email, re, os, difflib, smtplib, string, datetime, mimetypes
from time import localtime, strftime,gmtime
from pyelasticsearch import ElasticSearch
import json

from ConfigParser import SafeConfigParser

config = "/etc/oplog/oplog.cnf"
if os.path.exists(config):
        parser = SafeConfigParser()
        parser.read(config)
else:
        print "No config file found! Please create: %s" % config
        sys.exit(1)

basedir = parser.get('default', 'basedir').strip('"').strip("'")
baseurl = parser.get('default', 'baseurl').strip('"').strip("'")
elasticsearch = parser.get('default', 'elasticsearch').strip('"').strip("'")
txtlog = parser.get('default', 'txtlog').strip('"').strip("'")

# where to store mime attachments
attachdir = basedir + "/attachments/"

# where to store logs if we keep them
logdir = basedir + "/logs"

errMsg = 'Usage: ' + sys.argv[0] + ' [queue name]'
testres = len(sys.argv)
if testres < 2:
 print errMsg
 sys.exit(1)

queue = sys.argv[1]

debugmode = "F"

logdate = strftime("%Y%m%d", localtime())
oplogfile = logdir + "/opLog-" + logdate + ".log"
recdate = strftime("%a, %d %b %Y %H:%M:%S %Z", localtime())
subdate = strftime("%Y-%m-%dT%H:%M:%S", localtime())

def degbu(string):
	if debugmode == "T":
		print string

def sanitize(txt):
        txt = txt.replace("&", "&amp;")
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        txt = txt.replace("'", "&#039;")
        return txt

# read input from procmail
s = sys.stdin.read()
# parse message using the email module
msg = email.message_from_string(s)

if debugmode == "T":
	print msg.is_multipart()

msgdate = msg['Date']
msgsubject = sanitize(msg['Subject'])
msgfrom = sanitize(msg['From'])
okcontent = ["text/plain", "text/html"]
if msg.is_multipart() == True:
	counter = 1
	load = ""
	for part in msg.walk():
		# multipart/* are just containers
		if part.get_content_maintype() == 'multipart':
			continue
		filename = part.get_filename()
		if part.get_content_type() in okcontent:
			load += sanitize(part.get_payload())
			load += "\n"
		else: 
			ext = mimetypes.guess_extension(part.get_content_type())
			degbu("DEBUG ext: " + ext)
			if not ext:
				# Use a generic bag-of-bits extension
				ext = '.bin'
			shortext = filename[-4:]
			degbu("DEBUG SHORTEXT: " + shortext)
			if filename:
			 	shortname = filename[:-4]
			else:
				shortname = "part"
			degbu("DEBUG SHORTNAME: " + shortname)
			newfile = "%s%s-%d%s" % (attachdir, shortname, counter, shortext)
			degbu("DEBUG newfile: " + newfile)
			while os.path.exists(newfile) == True:
				degbu("DEBUG newfile: " + newfile + " exists. Incrementing")
				counter = counter +1
				newfile = "%s%s-%d%s" % (attachdir, shortname, counter, shortext)
			newshort = "%s-%d%s" % (shortname, counter, shortext)
			degbu("DEBUG newfile: " + newfile)
			fp = open(newfile, 'w')
			fp.write(part.get_payload(decode=True))
			fp.close()
			os.chmod(newfile, 0644)
			filestring = 'Attachment: <a href="%sattachments/%s">%s</a><br>\n' % (baseurl, newshort, newshort)
			load += filestring
else:
	load = msg.get_payload()

payload = load.rstrip("\n")
# attachment strings aren't sanitized, so we're doing this to keep them from breaking anything
payload = payload.replace("'", "&#039;")

# write the message to elasticsearch
if debugmode != "T":
	x = {'submitted': subdate, 'sent': msgdate, 'from': msgfrom, 'subject': msgsubject, 'body': payload }
	es = ElasticSearch(elasticsearch)
	print json.dumps(x)
	es.index("oplog", queue, x)

if txtlog == 'T':
	# write the message to the text log
	# we're reconstructing variables here because the formatting is different
	logsubject = msg['Subject']
	logfrom = msg['From'].replace("'", "")
	logpayload = load.rstrip("\n")
	logrecord = """System  date: %s\n
Message date: %s\n
Message from: %s\n
Message subject: %s\n
Message body:\n
%s\n\n
<----------------END MESSAGE ------------------------>\n\n""" % (recdate, msgdate, logfrom, logsubject, logpayload)
	degbu(logrecord)
	if debugmode != "T":
		log = open(oplogfile, 'a')
		log.write(logrecord)
		log.close()
