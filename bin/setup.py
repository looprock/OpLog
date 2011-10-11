#!/usr/bin/env python
import sys
sys.path.append('/opt/oplog/conf')
import oplog
import opdb
opdb = opdb.opdb()
opdb.setup()
opdb.createqueue("defaultqueue","Logs")
opdb.insert("insert into xmppusherlm values (1,0)")
opdb.close()
