#!/usr/bin/env python

# where you install oplog - DON'T CHANGE THIS!
# this is configured into all the scripts. Things will seriously break
# if you don't use /opt/oplog as your base directory
basedir = "/opt/oplog/"

# URL prefix uses for oplog, i.e. http://your.server/oplog/
baseurl = "http://10.211.55.19/oplog/"

# where to store mime attachments
attachdir = basedir + 'www/html/attachments/'

## Logging
# store logs (T/F)?
txtlog = 'T'
# where to store logs if we keep them
logdir = basedir + "logs"

# Mail settings

# mail relay (can be localhost)
mailhost="localhost"
# error handler address: were you want error notices to go to
mailfrom="oplog-errors@mail.com"
# addresses you want to receive error notices
mailerrto="oplog-err-handler@mail.com"
