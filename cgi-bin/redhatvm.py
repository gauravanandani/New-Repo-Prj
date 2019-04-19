#!/usr/bin/python

import os
import cgi
import mysql.connector as mariadb


conn=mariadb.connect(user='root', password='redhat', database='cloudvm')
cursor=conn.cursor()

print("Content-type:text/html")
print("")

web=cgi.FieldStorage()

name=web.getvalue('osname')
ram=web.getvalue('ram')
cpu=web.getvalue('cpu')
port=web.getvalue('port')
password=web.getvalue('pass')


#checking..
cursor.execute("flush privileges")
cursor.execute("select osname from novnc where osname='"+str(name)+"'")
a=cursor.fetchone()

if(a != None):
	if(a[0] == name):
		print "Name already Exist Try again"
		print "<meta http-equiv=refresh content=2;url=/redhatvm.html />"
else:

	#inserting information...
	try:
		cursor.execute("INSERT INTO novnc (osname,ram,cpu,port) VALUES (%s,%s,%s,%s)", (name,ram,cpu,port))
	except mariadb.Error as error:
		print("Error: {}",format(error))

	conn.commit()
	conn.close()

	#building process
	os.system("sudo qemu-img  create -f qcow2 -b  /var/lib/libvirt/images/rhvmdnd.qcow2 /var/lib/libvirt/images/"+ str(name) +".qcow2 &")

	os.system("sudo virt-install --name "+ str(name) +" --ram "+ str(ram) +" --vcpu "+ str(cpu) +" --disk path=/var/lib/libvirt/images/"+ str(name) +".qcow2 --import --graphics=vnc,listen=192.168.10.160,port=5994 --noautoconsole  &")
	try:
		os.system("nohup websockify --web=/usr/share/novnc "+ str(port) +" 192.168.10.160:5994  &")
	except socket.error as error2:
		print("Define Another Port number: {}",format(error2))
		
	print "<meta http-equiv=refresh content=2;url=http://192.168.10.160:"+str(port)+" />"

