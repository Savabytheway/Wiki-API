import sqlite3

connection = sqlite3.connect('requestshistorydata.sqlite')
cursr = connection.cursor()

cursr.executescript('''
DROP TABLE IF EXISTS Requests;
CREATE TABLE "Requests" (
	"id"	INTEGER NOT NULL UNIQUE,
	"request"	TEXT,
	"region"	TEXT,
	"year"	TEXT,
	"views"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
''')