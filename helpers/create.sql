create table queues (
id int(100) auto_increment NOT NULL,
dbname varchar(50) NOT NULL,
title varchar(50) NOT NULL,
PRIMARY KEY(id)
);

insert into queues (dbname,title) values ('defaultqueue','Logs');

create table defaultqueue (
id int(100) auto_increment NOT NULL,
recdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
mailfrom varchar(200) NOT NULL,
maildate varchar(50) NOT NULL,
msgsubject TEXT NOT NULL,
msgbody LONGTEXT NOT NULL,
PRIMARY KEY (id)
);
