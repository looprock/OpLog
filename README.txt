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
apache (for the cgi)
python MySQLdb
procmail
some MTA
(python xmpppy and pydns for xmpp based notification)

------------------------------------------------------------------------------

Installation:

1. put contents of oplog-0.2.tar.gz in /opt/oplog (or symlink or whatever)

2. configure mysql DB (something like...):
mysqladmin -u root -p create oplog
GRANT ALL ON oplog.* TO oplog@localhost IDENTIFIED BY 'password_here';
mysql -u oplog -p oplog < /opt/oplog/helpers/create.sql

3. add user oplog, chown /opt/oplog to oplog, and ensure that user can get email

4. configure oplog.py:
This is the main configuration file used by all the components of oplog.
This MUST live under /opt/oplog/conf/oplog.py. Depending on what features
you want, you might not need to configure the whole thing to get rolling, 
i.e. if you don't enable the xmpp pusher script in cron that section isn't
needed.

5. set up procmail:
Create the directories "mail" and ".mailproc" under the user oplog's home 
directory

copy the helpers/procmailrc to .procmailrc under  the user oplogs's home 
directory

[ At this point you should be logging email messages sent to the oplog user 
account ]

6. link (or copy) /opt/oplog/conf/http_oplog.conf to /etc/httpd/conf.d or 
appropriate apache config directory. This assumes everything is set up under
/opt/oplog and the oplog baseurl is http:// your.server/oplog

[ at this point you should be able to see any messages you've sent to oplog ]

7. configure clients
Set the appropriate server string to reach the oplogger soap service in:
/opt/oplog-0.2/www/html/app/OS_X/python/opLogger
/opt/oplog-0.2/www/html/app/Win32/python/opLogger.py

Try installing one of the clients and see if it works!

8. set up cron jobs:
# this job will mail errors to the error handler set in in oplog.py and do
# some basic house cleaning
0 0 * * * /opt/oplog/bin/mailerrs.py > /dev/null 2>&1

# this job ensures the text logs are readable from a browser
*/5 * * * * chmod +r /opt/oplog/logs/*.log> /dev/null 2>&1

9. Optional: configure the xmppusher script for xmpp notifications
create a jabber user through the traditional method, and log out
make sure you've configured the xmpp setup section in oplog.py
enable the cron job:
* * * * * /opt/oplog/bin/xmppusher > /dev/null 2>&1

Bugs:

Messages with attachments won't log to oplog. It's a known bug and I hope to
address it at some point

OS X widget:
I've included the dashcode project files under the helpers directory in both
the standard and long formats for anyone who wants to build a oplog dashboard
widget. They're based on the sample RSS reader widget and all you should need
to do is modify the URL to match your configuration.

--Douglas Land (doug.land@nokia.com)
