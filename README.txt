About:
------------------------------------------------------------------------------
OpLog is a message broadcast service for our various monitors, notifications,
etc.; think twitter for sysadmins.

The main goal for OpLog was to replace email as the main client for
notifications. Operations e-mail accounts are constantly filling up with
things we may and or may not care about, numbing us and eventually causing us
to stop paying attention to most emails we get. This also costs us time and
energy cleaning up our mailboxes on a regular basis.

OpLog is designed to be a minimally intrusive system. The current client
notifications can be passively disregarded or looked into further if more
details are desired.

The current interfaces for OpLog are:
*      The cgi you're about to set up
*      Omnigrowl/Snarl notifications
*      RSS feed (and associated Dashboard widget)
*      Via your Jabber/XMPP capable IM client

To fit into our current infrastructure, the input mechanism that was chosen
for OpLog was email. To "port" an application to use OpLog notifications, you
only need to add the appropriate e-mail address as a recipient.

------------------------------------------------------------------------------

Requirements:

python >= 2.3.4
apache with cgi support
python MySQLdb
sendmail (but really any MTA will work)
(python xmpppy and pydns for xmpp based notification)

------------------------------------------------------------------------------

Installation:

1. put contents in /opt/oplog (or symlink)

2. configure mysql DB (something like...):
mysqladmin -u root -p create oplog
then log into mysql and run:
GRANT ALL ON oplog.* TO oplog@localhost IDENTIFIED BY 'password_here';
flush privileges;

3. configure oplog.py:
This is the main configuration file used by all the components of oplog.
This MUST live under /opt/oplog/conf/oplog.py. Depending on what features
you want, you might not need to configure the whole thing to get rolling, 
i.e. if you don't enable the xmpp pusher script in cron that section isn't
needed.
Lastly, run: /opt/oplog/bin/setup.py to populate the database.

4. configure sendmail:
Assuming you're using smrsh, symlink /opt/oplog/bin/oplog_mailparser.py
under /etc/smrsh/, then create an alias in /etc/aliases
oplog: 	"|/etc/smrsh/oplog_mailparser.py 1"
Then run "newaliases".

in this line, the 1 at the end specifies the queue you want to send mail to.
You can create multiple queues using: /opt/oplog/bin/queues/create_queue
You can verify the queue ID to use in aliase with:
/opt/oplog/bin/queues/show_queues
A default queue with id 1 will be created when you run the create.sql script
with the name defaultqueue and title "Logs". If you want you rename this
queue you can use: /opt/oplog/bin/queues/change_queue_title.

To create additional queues, just use the create_queue command and add 
a new entry in /etc/aliases with the appropriate queue ID.

[ This will work similarly under postfix once you get the aliases set. ]

5. link (or copy) /opt/oplog/conf/http_oplog.conf to /etc/httpd/conf.d or 
appropriate apache config directory. This assumes everything is set up under
/opt/oplog and the oplog baseurl is http://your.server/oplog

[ at this point you should be able to see any messages you've sent to oplog ]

6. configure clients
Set the appropriate server string to reach the oplogger soap service in:
/opt/oplog-0.2/www/html/app/OS_X/python/opLogger
/opt/oplog-0.2/www/html/app/Win32/python/opLogger.py
Don't forget to change/set the queue and server variables in these scripts!

Try installing one of the clients and see if it works!

7. Optional: configure the xmppusher script for xmpp notifications
create a jabber user through the traditional method, and log out
make sure you've configured the xmpp setup section in oplog.py
enable the cron job:
* * * * * /opt/oplog/bin/xmppusher [queue]> /dev/null 2>&1
r.e. if you want to set it for the default queue:
* * * * * /opt/oplog/bin/xmppusher 1> /dev/null 2>&1

OS X widget:
I've included the dashcode project files under the helpers directory in both
the standard and long formats for anyone who wants to build a oplog dashboard
widget. They're based on the sample RSS reader widget and all you should need
to do is modify the URL to match your configuration.
