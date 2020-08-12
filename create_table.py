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

'''Create the email table. This table contains information for all comments
that people send us.'''

"""Create the table for the database."""
def main():
	def comment_table(db, conn, c):
		__tablename__ = 'Email_Info'
		Name = Column(String)
		Cust_id = Column(Integer)
		Email_Address = Column(String)
		Comment = Column(String)
		Time_stamp = Column(DateTime)
		

		c.execute('CREATE TABLE IF NOT EXISTS `Email_Info`\
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

		c.execute('CREATE TABLE IF NOT EXISTS `Login`\
			(Id NUMERIC PRIMARY KEY, \
			email Text, \
			Password Text, \
			rec_type Text, \
			Time_stamp Datetime)')

		conn.commit()

	def reference_id(db, conn, c):
		__tablename__ = 'reference_id'
		id = Column(Integer, primary_key = True)
		Time_stamp = Column(DateTime)

		c.execute('CREATE TABLE IF NOT EXISTS `reference_id`\
			(Id NUMERIC PRIMARY KEY, \
			Time_stamp Datetime)')

		conn.commit()


	def customer_master(db, conn, c):
		__tablename__ = 'customer_master'
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

		c.execute('CREATE TABLE IF NOT EXISTS `Customer_Master`\
			(Cust_Id NUMERIC PRIMARY KEY, \
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

		c.execute('CREATE TABLE IF NOT EXISTS `Employee_Master`\
			(ee_id NUMERIC PRIMARY KEY, \
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
		master_account_id = Column(Integer)
		account_number = Column(Integer)
		cust_id = Column(Integer),
		account_balance = Column(Float)
		Time_stamp = Column(DateTime)

		c.execute('CREATE TABLE IF NOT EXISTS `account_master`\
			(master_account_id NUMERIC, \
			account_number NUMERIC, \
			account_balance NUMERIC, \
			cust_id NUMERIC, \
			Time_stamp Datetime, \
			PRIMARY KEY (master_account_id, account_number))')

		conn.commit()


	def journal_entry(db, conn, c):
		__tablename__ = 'journal_entries'
		Date_of_entry = Column(Date)
		cust_id = Column(String)
		master_account_id = Column(String)
		account_number = Column(String)
		Debit_amount = Column(Float)
		Credit_amount = Column(Float)
		Description = Column(Text)
		Ee_id = Column(Text)
		ticker_symbol = Column(Text)
		Time_stamp = Column(DateTime)


		c.execute('CREATE TABLE IF NOT EXISTS `journal_entries`\
			(Date_of_entry Date, \
				master_account_id TEXT, \
				cust_id TEXT, \
				account_number TEXT, \
				Debit_amount Numeric, \
				Credit_amount NUMERIC, \
				Description Text,\
				ee_id Text, \
				ticker_symbol Text, \
				Time_stamp Datetime, \
				PRIMARY KEY (ee_id, Time_stamp))')
		conn.commit()

	def historical_data(db, conn, c):
		conn_ft = http.client.HTTPSConnection("ftl.fasttrack.net")
		headers = {
			'appid': reference.appid,
			'token': reference.token
		}
		# Get historical data - daily price closing history
		table_name = 'price_history'
		for sec in reference.sec_list:
			# conn_ft.request("GET", "/v1/data/" + sec + "/range?start=1%2F1%2F2000&end=7%2F20%2F2020&adj=&olhv=0", headers=headers)
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

				c.execute('CREATE TABLE IF NOT EXISTS ' + table_name + '\
					(As_of_Date DATE, \
					Sec TEXT, \
					Price NUMERIC, \
					Count Numeric, \
					Time_stamp Datetime, \
					UNIQUE (As_of_Date, Sec))')
				c.execute('INSERT INTO ' + table_name + ' VALUES(?, ?, ?, ?, ?)', list_col)
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

				c.execute('CREATE TABLE IF NOT EXISTS Sec_Info (Ticker String PRIMARY KEY, \
					Name String, \
					Category String, \
					Time_stamp Datetime)')
				try:
					c.execute('INSERT INTO Sec_Info VALUES(?, ?, ?, ?)', list_col)
				except:
					pass
			conn.commit()


	##### start running code #####
	# Create connection to sqlite3
	engine = create_engine('sqlite:///roboinvest.db')
	Base = declarative_base()
	conn = sqlite3.connect(reference.database)
	c = conn.cursor()

	# Create datbase tables
	comment_table(reference.database, conn, c)
	print('success creating comment table')
	login(reference.database, conn, c)
	print('Success creating login table')
	reference_id(reference.database, conn, c)
	print('Success creating reference database')
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

	# Populate reference table with id = 1
	time_stamp = datetime.now()
	id = 1
	datalist = [id, time_stamp]
	c.execute('INSERT INTO `reference_id` VALUES(?, ?)', datalist)
	conn.commit() 
	# Set password in account master to be the character '*'

	# Close connection to database
	c.close()


if __name__ == "__main__":
	main()
