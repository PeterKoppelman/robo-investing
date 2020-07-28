from datetime import datetime
from sqlalchemy import Column, Date, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3

import http.client
import json

import sys

sys.path.insert(1, '/users/pkopp/python_diploma/Capstone/prod/apps')
import reference

'''Create the email table. This table contains information for all comments
that people send us.'''

"""Create the table for the database."""
def main():
	def comment_table(db, conn, c):
		__tablename__ = 'Email_Info'
		Name = Column(String, primary_key = True)
		Email_Address = Column(String)
		Comment = Column(String)
		Timestamp = Column(String)
		

		c.execute('CREATE TABLE IF NOT EXISTS `Email_Info`\
		    (Name TEXT PRIMARY KEY, Email_Address TEXT, \
		    Comment TEXT, Timestamp TEXT)')

		conn.commit()

	def login(db, conn, c):
		__tablename__ = 'Login'
		Id = Column(String, primary_key = True)
		Password = Column(String)
		Name = Column(String)
		Timestamp = Column(Date)

		c.execute('CREATE TABLE IF NOT EXISTS `Login`\
		    (Id TEXT PRIMARY KEY, Password Text, Name Text, Timestamp TEXT)')

		conn.commit()


	def account_opening(db, conn, c):
		__tablename__ = 'account_master'
		First_Name = Column(String)
		Middle_initial = Column(String)
		Last_name = Column(String, primary_key = True)
		Street_addr = Column(String)
		City = Column(String)
		State = Column(String)
		Zip_code = Column(String)
		Email_addr = Column(String)
		TIN = Column(String)
		DOB = Column(String)
		Timestamp = Column(Date)

		c.execute('CREATE TABLE IF NOT EXISTS `Account_Master`\
		    (First_name Text, Middle_initial TEXT, Last_name Text PRIMARY KEY,\
		    	Street_addr Text, City Text, State Text, Zip_code Text,\
		    	Email_addr Text, TIN Text, DOB Text, Timestamp TEXT)')

		conn.commit()


	def historical_data(db, conn, c):
		conn_ft = http.client.HTTPSConnection("ftlightning.fasttrack.net")
		headers = {
			'appid': reference.appid,
			'token': reference.token
		}
		# sec_list = ["VOO", "PRULX", "VTIAX", "PFORX", "FDHY", "SPY"]
		table_name = 'price_history'
		for sec in reference.sec_list:
			sec_data = []
			conn_ft.request("GET", "/v1/data/" + sec + "/range?start=1%2F1%2F2000&end=7%2F20%2F2020&adj=&olhv=0", headers=headers)
			res = conn_ft.getresponse()
			data = res.read()
			dic = json.loads(data)
			for ix in range(len(dic['datarange'])):
				list_col = []
				list_col = [dic['datarange'][ix]['date']['strdate'], 
					sec, 
					dic['datarange'][ix]['price'],
					datetime.now()]

				c.execute('CREATE TABLE IF NOT EXISTS ' + table_name + '\
					(As_of_Date DATE, Sec TEXT, Price NUMERIC, Timestamp Date,\
					UNIQUE (As_of_Date, Sec))')
				c.execute('INSERT INTO ' + table_name + ' VALUES(?, ?, ?, ?)', list_col)
				conn.commit()


	##### start running code #####
	# Create connection to sqlite3
	engine = create_engine('sqlite:///roboinvest_prod.db')
	Base = declarative_base()
	conn = sqlite3.connect(reference.database)
	c = conn.cursor()

	# Create datbase tables
	comment_table(reference.database, conn, c)
	print('success creating comment table')
	login(reference.database, conn, c)
	print('Success creating login table')
	account_opening(reference.database, conn, c)
	print('Success creating account_opening table')
	historical_data(reference.database, conn, c)
	print('success creating and populating historical data table')

	# Close connection to database
	c.close()


if __name__ == "__main__":
    main()
