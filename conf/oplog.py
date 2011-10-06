#!/usr/bin/env python

# where you install oplog - DON'T CHANGE THIS!
# this is configured into all the scripts. Things will seriously break
# if you don't use /opt/oplog as your base directory
basedir = "/opt/oplog/"
# URL prefix uses for oplog, i.e. http://your.server/oplog/
baseurl = "http://[your.url.here]/oplog/"
# temp location
tmpdir = basedir + 'tmp/'
# where to store mime attachments
attachdir = basedir + 'www/html/attachments/'

# enable/disable text logging
txtlog = "T"

# the first day oplog will show in it's day view. When you hit this date
# no "<" arrow will be presented. This can also be used to mask testing
# testing data before you go "live" w/o clearing the DB
oplog_start_date = "2007-09-08"

# Main oplog database information

# to use unix socket, set db_host "localhost" and db_port "3306"
db_host = "localhost"
db_port = "3306"
db_username = "oploguser"
db_password = "oplogpass"
db_name = "oplog"

# Notification settings
# these are used by the xmppusher script

# We use a contacts database among multiple apps. The work-around for
# environments without this is to set notify_db_enabled "false".  The
# xmpp notification script will then use the xmpp_notified list below for 
# accounts is should send notices to.

notify_db_enabled = "true"
# to use unix socket, set db_host "localhost" and db_port "3306"
notify_db_host = "mysql.com"
notify_db_port = "3306"
notify_db_username = "contactuser"
notify_db_password = "contactpass"
notify_db_name = "contacts"

# this list will get used if notify_db_enabled set to false
# so far jabber.org and livejournal accounts have been tested
# unfortunately there's a problem accessing gtalk accounts
xmpp_notified = ['user@jabber.org', 'user@livejournal.com']

# XMPP username and password of account that will be doing the IMing
xmpp_username = "nokmaps@jabber.org/Work"
xmpp_password = "nmpasswd"
xmpp_sasl = 1
xmpp_security = 0

# Mail settings

# mail relay (can be localhost)
mailhost="mail.com"
# error handler address: were you want error notices to go to
mailfrom="oplog-errors@mail.com"
# addresses you want to receive error notices
mailerrto="oplog-err-handler@mail.com"

# Error collection Settings

# local mailbox file written to if parser fails.
# DEFAULT in .profmailrc
mailbox_file="/home/oplog/mail/mbox"
# LOGFILE in .profmailrc
mailbox_log="/home/oplog/.mailproc/log"