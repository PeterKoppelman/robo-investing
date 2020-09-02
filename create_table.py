from datetime import datetime
from sqlalchemy import Column, Date, String, create_engine,\
	Float, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3

import http.client
import json

import sys

sys.path.insert(1, '/roboinvest/apps')
# sys.path.insert(1, '/Users/pkopp/python_diploma/capstone/dev/apps')
import reference

'''Create the email table. This table contains information for all comments
that people send us.'''

"""Create the table for the database."""
def main():
	def comment_table(db, conn, c):
		__tablename__ = 'Email_Info'
		Name = Column(String)
		Email_Address = Column(String)
		Comment = Column(String)
		Time_stamp = Column(DateTime)
		

		c.execute('CREATE TABLE IF NOT EXISTS Email_Info\
			(Name TEXT, \
			Email_Address TEXT, \
			Comment TEXT, \
			Time_stamp Datetime)')

		conn.commit()

	def login(db, conn, c):
		__tablename__ = 'Login'
		cust_id = Column(Integer, primary_key = True)
		email = Column(String)
		Password = Column(String)
		rec_type = Column(String)
		Time_stamp = Column(DateTime)

		c.execute('CREATE TABLE IF NOT EXISTS Login\
			(Id NUMERIC PRIMARY KEY, \
			email Text, \
			Password Text, \
			rec_type Text, \
			Time_stamp Datetime)')

		conn.commit()

	def customer_master(db, conn, c):
		__tablename__ = 'Customer_master'
		cust_id = Column(Integer, primary_key = True)
		First_Name = Column(String)
		Middle_initial = Column(String)
		Last_name = Column(String)
		Street_addr = Column(String)
		City = Column(String)
		State = Column(String)
		Zip_code = Column(String)
		Email_addr = Column(String)
		TIN = Column(String)
		DOB = Column(String)
		Time_stamp = Column(DateTime)

		c.execute('CREATE TABLE IF NOT EXISTS Customer_Master\
			(Cust_Id Integer  PRIMARY KEY, \
				First_name Text Not Null, \
				Middle_initial TEXT Null, \
				Last_name Text Not Null,\
				Street_addr Text Not Null, \
				City Text Not Null, \
				State Text Not Null, \
				Zip_code Text Not Null,\
				Email_addr Text Not Null, \
				TIN Text Not Null, \
				DOB Text Not Null, \
				Time_stamp Datetime Not Null)')

		conn.commit()

	def employee_master(db, conn, c):
		__tablename__ = 'employee_master'
		ee_id = Column(Integer, primary_key = True)
		First_Name = Column(String)
		Middle_initial = Column(String)
		Last_name = Column(String)
		Street_addr = Column(String)
		City = Column(String)
		State = Column(String)
		Zip_code = Column(String)
		Email_addr = Column(String)
		TIN = Column(String)
		DOB = Column(String)
		Time_stamp = Column(DateTime)

		c.execute('CREATE TABLE IF NOT EXISTS Employee_Master\
			(ee_id Integer PRIMARY KEY, \
				First_name Text, \
				Middle_initial TEXT, \
				Last_name Text,\
				Street_addr Text, \
				City Text, \
				State Text, \
				Zip_code Text,\
				Email_addr Text, \
				TIN Text, \
				DOB Text, \
				Time_stamp Datetime)')

		conn.commit()

	def account_master(db, conn, c):
		__tablename__ = 'account_master'
		cust_id = Column(Integer),
		account_number = Column(Integer)
		account_balance = Column(Float)
		Time_stamp = Column(DateTime)

		c.execute('CREATE TABLE IF NOT EXISTS account_master\
			(cust_id Integer, \
			account_number Integer, \
			account_balance Float, \
			Time_stamp Datetime, \
			PRIMARY KEY (cust_id, account_number))')

		conn.commit()


	def journal_entry(db, conn, c):
		__tablename__ = 'journal_entries'
		Date_of_entry = Column(Date)
		cust_id = Column(Integer)
		account_number = Column(Integer)
		transaction_type = Column(Text)
		transaction_amount = Column(Float)
		ee_id = Column(Integer)
		ticker_symbol = Column(Text)
		Time_stamp = Column(DateTime)


		c.execute('CREATE TABLE IF NOT EXISTS journal_entries\
			(Date_of_entry Date, \
				cust_id Integer, \
				account_number TEXT, \
				transaction_type TEXT, \
				transaction_amount NUMERIC, \
				ee_id Integer, \
				ticker_symbol Text, \
				Time_stamp Datetime, \
				PRIMARY KEY (cust_id, account_number,Time_stamp))')
		conn.commit()

	def historical_data(db, conn, c):
		conn_ft = http.client.HTTPSConnection("ftl.fasttrack.net")
		headers = {
			'appid': reference.appid,
			'token': reference.token
		}
		# Get historical data - daily price closing history
		for sec in reference.sec_list:
			conn_ft.request("GET", "/v1/data/" + sec + "/range?start=1%2F1%2F2000&adj=&olhv=0", headers=headers)
			res = conn_ft.getresponse()
			data = res.read()
			dic = json.loads(data)
			count = 1
			for ix in range(len(dic['datarange'])):

				list_col = []
				list_col.append(dic['datarange'][ix]['date']['strdate'])
				list_col.append(sec)
				list_col.append(dic['datarange'][ix]['price'])
				list_col.append(count)
				list_col.append(datetime.now())

				c.execute('CREATE TABLE IF NOT EXISTS price_history \
					(As_of_Date DATE NOT NULL, \
					Sec TEXT NOT NULL, \
					Price Numeric NOT NULL, \
					Count Integer NOT NULL, \
					Time_stamp Datetime, \
					Unique(As_of_Date, Sec, Price, Count))')
				c.execute('INSERT INTO price_history VALUES (?, ?, ?, ?, ?)', list_col)
				count += 1
			conn.commit()

			# header data for securities. Name, category, etc.
			conn_ft = http.client.HTTPSConnection("ftl.fasttrack.net")
			for sec in reference.sec_list:
				list_col = []
				list_col.append(sec)

				conn_ft.request("GET", "/v1/data/" + sec + "/symname", headers=headers)
				res = conn_ft.getresponse()
				list_col.append(json.loads(res.read())['name'])

				conn_ft.request("GET", "/v1/ref/" + sec + "/details", headers=headers)
				res = conn_ft.getresponse()
				list_col.append(json.loads(res.read())['category'])
				list_col.append(datetime.now())

				c.execute('CREATE TABLE IF NOT EXISTS Sec_Info \
					(Ticker String PRIMARY KEY, \
					Name String NOT Null, \
					Category String NOT Null, \
					Time_stamp Datetime Not Null)')
				try:
					c.execute('INSERT INTO Sec_Info VALUES(?, ?, ?, ?)', list_col)
				except:
					pass
			conn.commit()


	##### start running code #####
	# Create connection to sqlite3
	engine = create_engine('sqlite:///roboinvest.db', echo = True)
	Base = declarative_base()
	conn = sqlite3.connect(reference.database)
	c = conn.cursor()

	# Create datbase tables
	comment_table(reference.database, conn, c)
	print('success creating comment table')
	login(reference.database, conn, c)
	print('Success creating login table')
	customer_master(reference.database, conn, c)
	print('Success creating customer master table')
	employee_master(reference.database, conn, c)
	print('Success creating employee master table')
	account_master(reference.database, conn, c)
	print('Success creating account master table')
	journal_entry(reference.database, conn, c)
	print('Success creating journal entry table')
	historical_data(reference.database, conn, c)
	print('Success creating and populating historical data table')

	# Close connection to database
	c.close()


if __name__ == "__main__":
	main()
