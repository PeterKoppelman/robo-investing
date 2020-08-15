# insert sample data in the roboinvest system
from datetime import datetime
from sqlalchemy import Column, Date, String, create_engine,\
	Float, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3

import http.client
import json

import sys

sys.path.insert(1, '/users/pkopp/python_diploma/Capstone/dev/apps')
import reference

# Create connection to sqlite3
engine = create_engine('sqlite:///roboinvest.db')
Base = declarative_base()
conn = sqlite3.connect(reference.database)
c = conn.cursor()
time_stamp = datetime.now()

# Account Master
datalist = ['1', '1', '0', '1', time_stamp ]
c.execute('INSERT INTO `account_master` VALUES(?, ?, ?, ?, ?)', datalist)

# Customer Master
datalist = ['1', 'John', ' ', 'Smith', '123 Main Street', 'New York', 'New York', '10001', 
	'pbkoppelman@gmail.com', '123456789', '01/01/2000', time_stamp]
c.execute('INSERT INTO `customer_master` VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', datalist)

# Employee Master
datalist = ['1', 'Peter', ' ', 'Koppelman', '320 Central Park West Apt 9G', 'New York', 'New York',
	 '10025', 'pkoppelman@yahoo.com', '123123123', '01/04/1958', time_stamp]
c.execute('INSERT INTO `employee_master` VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', datalist)

conn.commit()