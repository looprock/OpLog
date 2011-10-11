#!/usr/bin/env python
import sys
sys.path.append('/opt/oplog/conf')
import oplog
import opdb
opdb = opdb.opdb()
opdb.setup()
opdb.createqueue("defaultqueue","Logs")
opdb.insert("insert into xmppusherlm (queue) values (1)")
opdb.close()
