#!/usr/bin/env python
import oplog
import MySQLdb

class opdb(object):
	def __init__(self):
		if oplog.db_port == "3306":
			try:
				self.conn = MySQLdb.connect(host=oplog.db_host, user=oplog.db_username, passwd=oplog.db_password, db=oplog.db_name)
			except MySQLdb.Error, e:
				message = "Error %d: %s" % (e.args[0], e.args[1])
				print message
				sys.exit(1)
		else:
			try:
				self.conn = MySQLdb.connect(host=oplog.db_host, port=oplog.db_port, user=oplog.db_username, passwd=oplog.db_password, db=oplog.db_name)
			except MySQLdb.Error, e:
   				message = "Error %d: %s" % (e.args[0], e.args[1])
   				print message
   				sys.exit(1)

	def getdbbyid(self, str):
		curs = self.conn.cursor()
		curs.execute("select dbname from queues where id = %s", int(str))
		self.conn.commit()
		result = curs.fetchall()
		return result[0][0]

	def gettitlebyid(self, str):
                curs = self.conn.cursor()
                curs.execute("select title from queues where id = %s", int(str))
                self.conn.commit()
                result = curs.fetchall()
                return result[0][0]

        def getdbbytitle(self, str):
		curs = self.conn.cursor()
                curs.execute("select dbname from queues where title = '%s'", str)
                self.conn.commit()
                result = curs.fetchall()
                return result[0][0]

	def insert(self, statement):
		curs = self.conn.cursor()
		curs.execute(statement)
		self.conn.commit()

	def select(self, statement):
		curs = self.conn.cursor()
		curs.execute(statement)
		self.conn.commit()
		result = curs.fetchall()
		return result

	def close(self):
		self.conn.close()

	def createqueue(self, dbname, title):
		curs = self.conn.cursor()
		sql = "insert into queues (dbname,title) values ('%s','%s')" % (dbname,title)
		curs.execute(sql)
		self.conn.commit()
		sql = """create table %s (
id int(100) auto_increment NOT NULL,
recdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
mailfrom varchar(200) NOT NULL,
maildate varchar(50) NOT NULL,
msgsubject TEXT NOT NULL,
msgbody LONGTEXT NOT NULL,
PRIMARY KEY (id));""" % dbname
		curs.execute(sql)
		self.conn.commit()
