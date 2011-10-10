#!/usr/bin/env python
# version: 0.2
import xmlrpclib, PySnarl, os, sys

queue = 1

cachefile = "C:\opLog\cache.txt"
server = xmlrpclib.Server('http://[some.host.com]/oplog/cgi-bin/oplog_server.py')
lastmsg = server.getanswer(queue)[0][0]


result = os.path.exists(cachefile)

if result != 1:
    cachehandle = open(cachefile, 'w')
    cachehandle.write(str(lastmsg))
    cachehandle.close()
    id = PySnarl.snShowMessage("opLog Message", "Initialized cache. You'll be notified of new message from this point!", timeout=30)
        
cachehandle = open(cachefile, 'r')
currentmsg = cachehandle.readline()
cachehandle.close()


if int(currentmsg) != lastmsg:
    newrange = []
    for i in range((int(currentmsg) + 1),lastmsg):
        newrange.append(i)

    if len(newrange) > 10:
        lowrange = lastmsg - 10
    else:
        lowrange = lastmsg - len(newrange)

    for i in range(lowrange, lastmsg + 1):
        foo = server.getsubject(queue, str(i))
        id = PySnarl.snShowMessage("opLog Message", foo[0][0], timeout=5)

    cachehandle = open(cachefile, 'w')
    cachehandle.write(str(lastmsg))
    cachehandle.close()
