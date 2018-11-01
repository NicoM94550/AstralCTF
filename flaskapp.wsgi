#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")

from FlaskApp import app as application
application.secret_key = 'djhbfskjdhniu3y83hjk3imw7kyuwoefhkndkuasdhi76283yn983nym928dmy2983dhsoaidhsjnfhisukdfnhi8ywhkuddsfmnsdfmgjsdffffk'
