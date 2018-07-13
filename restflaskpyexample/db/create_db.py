import sqlite3

conn = sqlite3.connect('aw_site.db')
print "Opened database successfully";

conn.execute('CREATE TABLE aw_contact (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, email TEXT, phone TEXT, message TEXT)')
print "Table created successfully";
conn.close()
