#!/usr/bin/env python
# version: 0.0.7
import sys, email, MySQLdb, re, os, difflib, smtplib, string, datetime
from time import gmtime, strftime
sys.path.append('/opt/oplog/conf')
import oplog

logdate = strftime("%Y%m%d", gmtime())
oplogfile = oplog.basedir + "logs/opLog-" + logdate + ".log"
recdate = strftime("%a, %d %b %Y %H:%M:%S %Z", gmtime())

if oplog.db_port == "3306":
   conn = MySQLdb.connect(host=oplog.db_host, user=oplog.db_username, passwd=oplog.db_password, db=oplog.db_name)
else:
   conn = MySQLdb.connect(host=oplog.db_host, port=oplog.db_port, user=oplog.db_username, passwd=oplog.db_password, db=oplog.db_name)

# open the log file
log = open(oplogfile, 'a')
# read input from procmail
s = sys.stdin.read()
# parse message using the email module
msg = email.message_from_string(s)
msgdate = msg['Date']
logsubject = msg['Subject']
msgsubject = msg['Subject']
# format input with some search and replaces
msgsubject = msgsubject.replace("&", "&amp;")
msgsubject = msgsubject.replace('<', '&lt;')
msgsubject = msgsubject.replace('>', '&gt;')
msgsubject = msgsubject.replace('"', '&quot;')
msgsubject = msgsubject.replace("'", "&#039;")
logfrom = msg['From']
logfrom = logfrom.replace("'", "")
msgfrom = msg['From']
msgfrom = msgfrom.replace("&", "&amp;")
msgfrom = msgfrom.replace('<', '&lt;')
msgfrom = msgfrom.replace('>', '&gt;')
msgfrom = msgfrom.replace('"', '&quot;')
msgfrom = msgfrom.replace("'", "&#039;")
logpayload = msg.get_payload().rstrip("\n")
payload = msg.get_payload().rstrip("\n")
payload = payload.replace("&", "&amp;")
payload = payload.replace('<', '&lt;')
payload = payload.replace('>', '&gt;')
payload = payload.replace('"', '&quot;')
payload = payload.replace("'", "&#039;")
# write the message to the text log
log.write('System  date: ' + recdate + '\n')
log.write('Message date: ' + msgdate + '\n')
log.write('Message from: ' + logfrom + '\n')
log.write('Message subject: ' + logsubject + '\n')
log.write('Message body:\n')
log.write(logpayload + '\n')
log.write(' \n')
log.write('<----------------END MESSAGE ------------------------>\n')
log.write(' \n')
log.close()
# write the message to the database
curs = conn.cursor()
curs.execute('insert maillogs (maildate, mailfrom, msgsubject, msgbody) values (%s, %s, %s, %s)', (msgdate, msgfrom, msgsubject, payload))
conn.commit()
conn.close()
