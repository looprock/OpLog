#!/usr/bin/env python
# version: 0.1

import cgi, MySQLdb, datetime, time, SimpleXMLRPCServer, sys
sys.path.append('/opt/oplog/conf')
import oplog

# set up the database
import opdb
opdb = opdb.opdb()

# get all the elements passed to us via GET or POSTs
form = cgi.FieldStorage()
# and check how many of them there are
test_form=len(form)

# get the date today
todate = time.strftime("%Y%m%d")

# set the link and text colors
defaulttextcolor = "#525b5e"
defaultlinkcolor = "#999999"

# these display at the top and bottom of all pages
def mainlinks():
   print "<table border=0 cellspacing=1 cols=2 width=100%><tr>\n<td align=left>"
   print "<a href=\"index.py?queue=%s\">Home</a>" % (str(queue))
   print '| <a href="?action=about&queue=%s">About</a>' % (str(queue))
   print '| <a href="?action=apps&queue=%s">Support Applications</a>' % (str(queue))
   print '| <a href="?action=day&queue=%s">View By Day</a>' % (str(queue))
   print '| <a href="?action=search&queue=%s">Search</a>' % (str(queue))
   #print '| <a href="?action=textlogs&queue=%s">Text Logs</a>' % (str(queue))
   print '| <a href="?action=feed&queue=%s">RSS Feed</a>' % (str(queue))
   print "</td></tr></table><p>"

# shared top and bottom elements of all pages
def header():
  print "<b>Queues:</b>"
  qs = opdb.select("select * from queues")
  for x in range(0,len(qs)):
        print "<a href=\"index.py?queue=%s\">%s</a> | " % (str(qs[x][0]),qs[x][2])
  print "<p>"
  mainlinks()
  print "<table border=0 cellpadding=0 cellspacing=0 width=100%>"
  print "<tr><td width=5%>&nbsp;</td>"
  print "<td><table border=1 cellpadding=4><tr><td width=70% bgcolor=#FFFFFF>"

def footer():
  print "</td></tr></table></td><td width=25%>&nbsp;</td></tr></table>"
  mainlinks()

# the text log display page content
def textlogs():
  print "<h1>%s: Text Logs</h1>" % (qtitle)
  header()
  print "<p><a href=\"../logs/opLog-" + str(todate) + ".log\">Current Text Log</a></p>\n"
  print "<p><a href=\"../logs/\">All Text Logs</a></p>\n"
  footer()

# the about page content
def about():
  print "<h1>Welcome to OpLog</h1>"
  header()
  print """<p>OpLog is a message broadcast service for our various monitors, notifications, etc.; think twitter for sysadmins.</p>\n 
  <p>The main goal for OpLog was to replace email as the main client for notifications. Operations e-mail accounts are constantly filling up with things we may and or may not care about, numbing us and eventually causing us to stop paying attention to most emails we get. This also costs us time and energy cleaning up our mailboxes on a regular basis.</p>\n
  <p>OpLog is designed to be a minimally intrusive system. The current client notifications can be passively disregarded or looked into further if more details are desired.</p>\n

  <br>The current interfaces for OpLog are:</br>\n

  <br> * &nbsp;&nbsp;&nbsp;&nbsp; The web page</br>\n
  <br> * &nbsp;&nbsp;&nbsp;&nbsp; Omnigrowl/Snarl notifications</br>\n
  <br> * &nbsp;&nbsp;&nbsp;&nbsp; RSS feed (and associated Dashboard widget)</br>\n
  <br> * &nbsp;&nbsp;&nbsp;&nbsp; Via your XMPP capable IM client</br>\n
  <p>&nbsp;&nbsp;&nbsp;&nbsp;</p>\n

  <p>To start using one of the desktop-based OpLog clients, visit the <a href="?action=apps">Support Applications</a> Page.</p>\n

  <p>To fit into our current infrastructure, the input mechanism that was chosen for OpLog was email. To "port" an application to use OpLog notifications, you only need to add the appropriate e-mail address as a recipient.</p>\n

  <p><b>*</b> The OpLog service is currently only available when you're connected to the yav4 network with the exception of XMPP based notifications.</p>"""
  print "<p>&nbsp;&nbsp;&nbsp;&nbsp;</p>"
  footer()

# "index" page content, in general what pops up if you don't add an action= to
# the index.py url
def default():
  print "<h1>%s: Last 10 Messages</h1>" % (qtitle)
  header()
  # select the 10 most current entries from oplog db and show them
  sql ="select msgsubject, mailfrom, recdate, maildate, msgbody, id from " + dbname + " where mailfrom not like '%dsl@looprock.com%' and msgsubject not like '%mailing list memberships reminder%' order by recdate desc LIMIT 10"
  result = opdb.select(sql)
  # we already know there will be 10 entries in the dictionary, so we can cheat
  for n in range (0, 9):
    print "<hr width=50% align=left>\n"
    print "<b><font size=4>-- " + result[n][0] + "</font></b><br>\n"
    print "<b>From: " + result[n][1] + "</b><br>\n"
    print "<b>Received Date:</b> " + result[n][2].strftime("%A %B %d %I:%M:%S %p %Y") + " (Sent: " + result[n][3] + ")<br>\n"
    print "<b>Message Body:</b><br>\n"
    # Truncate any message bodies longer than 1000 characters and produce a 
    # link to the full version
    length=1000
    if len(result[n][4]) > length:
       print "<p><pre>" + result[n][4][:length] + " ... </pre></p>\n"
       print "<b> ... [ TRUNCATED : </b></p>"
       print "<b><a href=\"index.py?action=show&queue=" + queue + "&msgid=" + str(result[n][5]) + "\">View Full record</a> ] </b><br>\n"
    else:
       print "<pre>" + result[n][4] + "</pre><p>\n"
  footer()

# this produces the RSS feed
def feed():
 print "Content-type: text/xml\n"
 print "<rss version=\"2.0\">\n"
 print "<channel>\n"
 print "<title>IOps Logger</title>\n"
 print "<description>A description of your site</description>\n"
 print "<link>http://tool.yav4.com/iLog</link>\n"
 print "<copyright>this info is confidential yo!</copyright>\n"
 # select the 10 most current entries from oplog db and show them
 sql = "select msgsubject, mailfrom, recdate, maildate, msgbody, id from " + dbname + " where mailfrom not like '%dsl@looprock.com%' and msgsubject not like '%mailing list memberships reminder%' order by recdate desc LIMIT 10"
 result = opdb.select(sql)
 # we already know there will be 10 entries in the dictionary, so we can cheat
 for n in range (0, 9):
   print "<item>\n"
   print "<title>" + result[n][0] + "</title>\n"
   print "<description>" + result[n][4] + "</description>\n"
   print "<link>" + oplog.baseurl + "cgi-bin/index.py?action=show&amp;msgid=" 
   print result[n][5]
   print "</link>\n"
   print "<pubDate>" + result[n][2].strftime("%A %B %d %I:%M:%S %p %Y") + "</pubDate>\n"
   print "</item>\n"
 print "</channel>\n"
 print "</rss>\n"

# display a single message by ID
def show():
  # make sure they gave us a message ID to show
  if test_form < 2:
    print "<h1>Error retrieving message id.</h1>"
    mainlinks()
  else :
    # get the mesage ID from the GET to the cgi
    msgid = form['msgid'].value
    print "<h1>%s: Messages Number - %s</h1>" % (qtitle, msgid)
    header()
    # select the record for that message ID and display it
    sql = "select msgsubject, mailfrom, recdate, maildate, msgbody, id from " + dbname + " where id=" + msgid + " and mailfrom not like '%dsl@looprock.com%' and msgsubject not like '%mailing list memberships reminder%'"
    result = opdb.select(sql)
    print "<hr width=50% align=left>\n"
    print "<b><font size=4>-- " + result[0][0] + "</font></b><br>\n"
    print "<b>From: " + result[0][1] + "</b><br>\n"
    print "<b>Received Date:</b> " + result[0][2].strftime("%A %B %d %I:%M:%S %p %Y") + " (Sent: " + result[0][3] + ")<br>\n"
    print "<b>Message Body:</b><br>\n"
    print "<pre>" + result[0][4] + "</pre><p>\n"
    footer()

# display messages by day. 
# if no date provided, assume today
def day():
  # I could have saved myself a bit of grief here by using teh "%Y-%m-%d" for
  # everything, but live and learn 
  dparts = dstamp.split("-")
  reqday = datetime.date(int(dparts[0]), int(dparts[1]), int(dparts[2]))
  # get the +1 and -1 dates for the "<" and ">" links
  minusoneday = reqday + datetime.timedelta(days=-1)
  plusoneday = reqday + datetime.timedelta(days=1)
  print "<center><h1>%s: " % (qtitle)
  # don't display a "<" once you hit the oplog_start_date
  if dstamp != oplog.oplog_start_date:
    print "<a href=\"?action=day&queue=" + str(queue) + "&dstamp=" + str(minusoneday) + "\">< </a> "
  print dstamp
  # don't display a ">" if the date matches today, nothing will be there!
  if dstamp != time.strftime("%Y-%m-%d"):
    print " <a href=\"?action=day&queue=" + str(queue) + "&dstamp=" + str(plusoneday) + "\">> </a> "
  print "</h1></center>"
  header()
  print "<br>"
  # select all the record IDs for the requested date
  sql = "select id from " + dbname + " where mailfrom not like '%dsl@looprock.com%' and msgsubject not like '%mailing list memberships reminder%' and recdate like '%" + dstamp + "%' order by recdate"
  result = opdb.select(sql)
  if len(result) != 0:
     # if there are records, display them
     for msgid in result:
        resid = str(msgid[0])
        sql = "select msgsubject, mailfrom, recdate, maildate, msgbody, id from " + dbname + " where id='" + resid + "' order by id"
        recordinfo = opdb.select(sql)
        print "<hr width=50% align=left>\n"
        print "<b><font size=4>-- " + recordinfo[0][0] + "</font></b><br>\n"
        print "<b>From: " + recordinfo[0][1] + "</b><br>\n"
        print "<b>Received Date:</b> " + recordinfo[0][2].strftime("%A %B %d %I:%M:%S %p%Y") + " (Sent: " + recordinfo[0][3] + ")<br>\n"
        print "<a href=\"index.py?action=show&queue=" + queue + "&msgid=" + str(recordinfo[0][5]) + "\">View Full record</a><br>\n"
     footer()
  # if not, sorry!
  else:
     print "<b>Sorry, no records for this date</b><p>\n"

# display the search page
def search():
  print "<form action=\"index.py\" method=\"post\">\n"
  print "<input type=hidden name=action value=searchsub>"
  print "<h1>%s Search:</h1>\n" % (qtitle)
  mainlinks()
  print "<INPUT TYPE=text SIZE=30 MAXLENGTH=100 NAME=keyword><br>\n"
  print "[ Date search format: Y-M-D h:m:s ]<p>\n"
  print "<INPUT TYPE=submit value=Search>\n"

# display the results page
def searchsub():
  keyword = form['keyword'].value
  # we're formatting input into the database in the parser, so we need to 
  # format the request to match here
  keyword = keyword.replace("&", "&amp;")
  keyword = keyword.replace('<', '&lt;')
  keyword = keyword.replace('>', '&gt;')
  keyword = keyword.replace('"', '&quot;')
  keyword = keyword.replace("'", "&#039;")
  print "<h1>%s: Results for - %s</h1><br>\n" % (qtitle, keyword)
  header()
  # select anything and everything that might match
  select0 = "select id from " + dbname + " where recdate like '%" + keyword + "%' or mailfrom like '%" + keyword + "%' or msgbody like '%" + keyword + "%' or msgsubject like '%" + keyword + "%' or maildate like '%" + keyword + "%' order by recdate desc"
  recordids = opdb.select(select0)
  # how many things did we find?
  print "<p>Results: <b>" + str(len(recordids)) + "</b><p>\n"
  # as long as there are some, show them
  if len(recordids) != 0:
     select1 = "select msgsubject, mailfrom, recdate, maildate, msgbody, id from " + dbname + " where recdate like '%" + keyword + "%' or mailfrom like '%" + keyword + "%' or msgbody like '%" + keyword + "%' or msgsubject like '%" + keyword + "%' or maildate like '%" + keyword + "%' order by recdate desc"
     results = opdb.select(select1)
     for recordinfo in results:
       print "<hr width=50% align=left>\n"
       print "<b><font size=4>-- " + recordinfo[0] + "</font></b><br>\n"
       print "<b>From: " + recordinfo[1] + "</b><br>\n"
       print "<b>Received Date:</b> " + recordinfo[2].strftime("%A %B %d %I:%M:%S %p%Y") + " (Sent: " + recordinfo[3] + ")<br>\n"
       print "<a href=\"index.py?action=show&queue=" + queue + "&msgid=" + str(recordinfo[5]) + "\">View Full record</a><br>\n"
  footer()

# display the helper apps page
def apps():
  print "<h1>Support Applications</h1>"
  header()
  print """<p>OS X:</p>
	<br><a href="../app/OS_X/python/">Growl Notifier</a> - A client written in python that sends notifications via Growl to your desktop</br>"""
  #print "<br><a href="../app/OS_X/widget/">OpLog Widget</a> - A dashboard widget that displays the OpLog RSS feed</br>"""
  print """<p>&nbsp;</p>
	<p>Win32:</p>
	<br><a href="../app/Win32/">Snarl Notifier</a> - A client written in python that sends notifications via Snarl to your desktop</br>
	<p>&nbsp;</p>
	<p>XMPP:</p>
	<p>There is an iLog to jabber transport that runs as a client (same base code as the WIN32/OS X python client) once a minute and will post iLog messages to your xmpp compatable (jabber.org, livejournal, but not gtalk so far) IM account.</p>
	<br>Once you have your compatable account set up in your client, register it here:</br>
	<p><a href="http://machinfo.dev.sf.yav4.com/oplogxmpp.php">http://machinfo.dev.sf.yav4.com/oplogxmpp.php</a><p>
	<p>That's it. After that, you should start getting iLog messages via IM.</p>
  <p>&nbsp;</p>"""
  footer()


# if there aren't any args passed via GET, assume they just want the index page
if 'action' in form:
	action = form['action'].value
else :
	action = "default"

if 'queue' in form:
	queue = form['queue'].value
else:
	queue = 1

if 'dstamp' in form:
	dstamp = form['dstamp'].value
else :
	dstamp = time.strftime("%Y-%m-%d")


dbname = opdb.getdbbyid(queue)
qtitle = opdb.gettitlebyid(queue)

# we don't want to diplay a regular html header to an rss reader
if action != "feed" and action != "client":
  print "Content-type: text/html\n"
  print "<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/loose.dtd\">"
  print "<html>"
  print "<head>"
  print "<link rel=\"alternate\" type=\"application/rss+xml\" title=\"RSS\" href=\"index.py?action=feed\" />";
  print "<link rel=\"stylesheet\" href=\"../default.css\">"
  print "<title>OpLog</title>"
  print "</head>"
  print "<body link=" + defaultlinkcolor + " alink=" + defaultlinkcolor + " vlink=" + defaultlinkcolor + " text=" + defaulttextcolor + ">"
  print "<div id=\"content\">"
  print "<br>"

# display what is asked for
if action == "default":
   default()
elif action == "feed":
   feed()
elif action == "show":
   show()
elif action == "search":
   search()
elif action == "searchsub":
   searchsub()
elif action == "about":
   about()
elif action == "apps":
   apps()
elif action == "textlogs":
   textlogs()
elif action == "day":
   day()
else:
   print "<h1>action not defined.</h1>"
   mainlinks()

if action != "feed" and action != "client": 
  print "</div>" 
  print "</body>"
  print "</html>"

# close out the db
opdb.close()
