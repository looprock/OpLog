About:
------------------------------------------------------------------------------
OpLog is a message broadcast service for our various monitors, notifications,
etc.; think twitter for sysadmins.

The main goal for OpLog was to replace email as the main client for
notifications. Operations e-mail accounts are constantly filling up with
things we may and or may not care about, numbing us and eventually causing us
to stop paying attention to most emails we get. This also costs us time and
energy cleaning up our mailboxes on a regular basis.

------------------------------------------------------------------------------

Requirements:

python >= 2.6.6
postfix/sendmail (but really any MTA will work)
pyelasticsearch

------------------------------------------------------------------------------

Installation:

1. clone the repo

2. Move etc/oplog/oplog.conf to /etc/oplog and cofigure it
This is the main configuration file used by all the components of oplog.

3. configure MTA, and add an alias per queue:

sendmail only: symlink /opt/oplog/bin/oplog_mailparser.py under /etc/smrsh/ 
All MTAs: create an alias in /etc/aliases

oplog: 	"|/path/to/oplog_mailparser.py [queue name, r.e. ops or netops]"
Then run "newaliases".

4. chmod 777 or set proper ownerships of attachments and logs dirs

At this point you should be able to see any messages you've sent to oplog in elasticsearch. 
