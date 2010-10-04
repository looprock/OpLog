#!/usr/bin/env python
# version 0.1
import os, sys, smtplib, gzip, datetime, glob
from email.MIMEText import MIMEText
sys.path.append('/opt/oplog/conf')
import oplog

minone = str(datetime.date.today() + datetime.timedelta(days=-1))
minseven = str(datetime.date.today() + datetime.timedelta(days=-7))

def pymailer(subtype, mailbody):
    subject="opLog Error: " + subtype
    server = smtplib.SMTP(oplog.mailhost)
    msg = MIMEText(mailbody)
    msg["Subject"] = subject
    msg["From"]    = oplog.mailfrom
    msg["To"]      = oplog.mailerrto
    server.sendmail(oplog.mailfrom, [oplog.mailerrto], msg.as_string())
    server.quit()

def write_compressed_file(filename, data):  
    fd = gzip.GzipFile(filename=filename, mode='wb', compresslevel=9)  
    fd.write(data)  
    fd.close()

# if there's an mbox file, email that and the log to the error handler
# 	then archive compressed copies for reference if needed
# if there isn't an mbox file just compress the log and archive it
# if neither exist, there's probably something wrong, email about that
if os.path.exists(oplog.mailbox_file):
   f = open(oplog.mailbox_file)
   mbox = f.read()
   f.close()
   f = open(oplog.mailbox_log)
   mlog = f.read()
   f.close()
   mailbody = mlog + " \n \n" + mbox
   pymailer ("oplog parser processing errors", mailbody)
   write_compressed_file(oplog.tmpdir + "mbox-" + minone + ".gz", mbox)
   write_compressed_file(oplog.tmpdir + "log-" + minone + ".gz", mlog)
   os.remove(oplog.mailbox_file)
   os.remove(oplog.mailbox_log)
else:
   if os.path.exists(oplog.mailbox_file):
      f = open(oplog.mailbox_log)
      mlog = f.read()
      f.close()
      write_compressed_file(oplog.tmpdir + "log-" + minone + ".gz", mlog)    
      os.remove(oplog.mailbox_log)
   else:
      pymailer ("no procmail log found", "something might be amiss")
   
# Housekeeping. delete files after 7 days
oldlogs = glob.glob(oplog.tmpdir + '*' + minseven + '.gz')
if len(oldlogs) > 0:
   for logfile in oldlogs:
       os.remove(logfile)
