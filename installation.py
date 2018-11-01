import os
Check = True
while Check:
	adminEmail = raw_input("Please enter an admin email: ")
	emailCheck = raw_input("Please confirm the email: ")
	if adminEmail == emailCheck:
		Check = False
	else:
		print("The emails do not match. Please try again")
Check = True
while Check:
	try:
		Phone = int(raw_input("Please enter an admin phone number(used to received text updates for message board): "))
		PhoneCheck = int(raw_input("Please confirm the phone number: "))
		if adminEmail == emailCheck:
			Check = False
		else:
			print("The numbers do not match. Please try again")
	except:
		print("Please enter an integer.")
secretSauce = str(raw_input("Please enter a secret hash(should be long and complex, don't bother memorizing): "))
toCall = ["sudo apt-get upgrade",
		"sudo apt-get update",
		"sudo apt-get --yes --force-yes install apache2 mysql-client mysql-server",
		"sudo apt-get --yes --force-yes install libapache2-mod-wsgi",
		"sudo apt-get --yes --force-yes install python-pip",
		"pip install --upgrade pip",
		"pip install Flask",
		"sudo apt-get --yes --force-yes install python-dev libmysqlclient-dev",
		"pip install MySQL-python",
		"pip install wtforms",
		"pip install passlib",
		"sudo a2enmod wsgi",
		"sudo mkdir /var/www/FlaskApp",
		"ifconfig -a > ipaddr.txt",
		"touch /etc/apache2/sites-available/FlaskApp.conf",
		"sudo a2ensite FlaskApp",
		"service apache2 reload",
		"touch /var/www/FlaskApp/flaskapp.wsgi",
		"mysql -u root -p -e 'CREATE DATABASE AstralCTF;'"]
for x in toCall:
	os.system(x)
ipAddr = open('ipaddr.txt','r').read().split('inet addr:')[1].split(' ')[0]

toWrite = ("""<VirtualHost *:80>
	ServerName %s
	ServerAdmin %s
	WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
	<Directory /var/www/FlaskApp/FlaskApp/>
		Order allow,deny
		Allow from all
	</Directory>
	Alias /static /var/www/FlaskApp/FlaskApp/static
	<Directory /var/www/FlaskApp/FlaskApp/static/>
		Order allow,deny
		Allow from all
	</Directory>
	ErrorLog ${APACHE_LOG_DIR}/error.log
	LogLevel warn
	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>""" % (ipAddr,adminEmail))

File = open('/etc/apache2/sites-available/FlaskApp.conf','w+')
File.write(toWrite)
File.close()

toWrite = ("""#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")

from FlaskApp import app as application
application.secret_key = '%s'""" % secretSauce)

File = open('/var/www/FlaskApp/flaskapp.wsgi','w')
File.write(toWrite)
File.close()
Check = True
while Check:
	mysqlpasswd = raw_input("Please enter your mysqlpasswd: ")
	mysqlcheck = raw_input("Please confirm the password: ")
	if mysqlpasswd == mysqlcheck:
		Check = False
	else:
		print("The passwords do not match. Please try again")
File = open('AstralCTF/dbconnect.py','r')
Data = File.read().replace("MYSQLPASSWD",mysqlpasswd)
File.close()
File = open('AstralCTF/dbconnect.py','w')
File.write(Data)
File.close()
os.system("mv AstralCTF /var/www/FlaskApp")
os.system("mv /var/www/FlaskApp/AstralCTF /var/www/FlaskApp/FlaskApp")
os.system("sudo rm -rf ipaddr.txt")
os.system("service apache2 restart")
print("Setup finished.")
print("Now please add the files in the folder 'AstralCTF' to /var/www/FlaskApp/FlaskApp")
print("After adding said files navigate to /var/www/FlaskApp/FlaskApp and run 'setup.py'")
print("The strings printed out by 'setup.py' are used to register teams, don't lose them!")
print("Once that is done running execute the command 'service apache2 restart'")
print("Navigate to /var/www/FlaskApp/FlaskApp/Problems and run 'addProblem.py' now or at any time to add problems.")
print("You can now navigate to the IP address of your server on any computer and the competition will load.")
print("To reset teams and score, run 'setup.py'")
print("To add a problem, run 'addProblem.py'")
print("To remove a problem, run 'removeProblem.py'")
print("To add a single hash, navigate to 'YOUR-IP/admin/addhash' and enter the admin password.")
print("Your IP address is: %s" % ipAddr)
