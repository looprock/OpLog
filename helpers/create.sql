create table maillogs (
recordid int(100) auto_increment NOT NULL,
recdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
mailfrom varchar(200) NOT NULL,
maildate varchar(50) NOT NULL,
msgsubject TEXT NOT NULL,
msgbody LONGTEXT NOT NULL,
PRIMARY KEY (recordid)
);
