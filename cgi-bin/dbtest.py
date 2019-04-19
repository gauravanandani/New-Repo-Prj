#!/usr/bin/python

import mysql.connector as mariadb
import cgi


print("Content-type:text/html")
print("")

web=cgi.FieldStorage()

name=web.getvalue('osname')
ram=web.getvalue('ram')
cpu=web.getvalue('cpu')
port=web.getvalue('port')
conn=mariadb.connect(user='root', password='redhat', database='cloudvm')
cursor=conn.cursor()

#checking..
cursor.execute("select osname,port from novnc where osname='"+str(name)+"'")
a=cursor.fetchone()

if(a != None):
	if(a[0] == name):
		print "Name already Exist Try again"
		print "<a href=/redhatvm.html>click here to go back</a>"


#inserting information...
try:
	cursor.execute("INSERT INTO novnc (osname,ram,cpu,port) VALUES (%s,%s,%s,%s)", (name,ram,cpu,port))
except mariadb.Error as error:
	print ("The last inserted id was: ",cursor.lastrowid)

conn.close()

