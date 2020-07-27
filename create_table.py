from datetime import datetime
from sqlalchemy import Column, Date, String, create_engine
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
	def comment_table(db):
		# engine = create_engine('sqlite:///stocks.db')
		engine = create_engine('sqlite:///email_info.db')
		Base = declarative_base()
		# conn = sqlite3.connect('email_info.db')
		conn = sqlite3.connect(db)
		c = conn.cursor()

		__tablename__ = 'Email_Info'
		Primary = Column(Date, primary_key=True)
		Timestamp = Column(String)
		Email_Address = Column(String)
		Comment = Column(String)
		Name = Column(String)

		# SL_Table.__table__.create(bind=engine, checkfirst=True)
		c.execute('CREATE TABLE IF NOT EXISTS `Email_Info`\
		    (Primary_Key TEXT PRIMARY KEY, Timestamp TEXT, Email_Address TEXT, Comment TEXT, Name TEXT)')

		conn.commit()
		c.close()
		print('success creating comment table')

	def historical_data(db):
		engine = create_engine('sqlite:///roboinvest.db')
		Base = declarative_base()
		# conn_sql = sqlite3.connect('roboinvest.db')
		conn_sql = sqlite3.connect(db)
		c = conn_sql.cursor()
		now = str(datetime.now()).replace(':', '-').replace(' ', '-').replace('.', '-')
		timestamp = datetime.now()
		conn = http.client.HTTPSConnection("ftlightning.fasttrack.net")
		headers = {
			'appid': reference.appid,
			'token': reference.token
		}
		sec_list = ["VOO", "PRULX", "VTIAX", "PFORX", "FDHY", "SPY"]
		for sec in sec_list:
			sec_data = []
			conn.request("GET", "/v1/data/" + sec + "/range?start=1%2F1%2F2000&end=7%2F20%2F2020&adj=&olhv=0", headers=headers)
			res = conn.getresponse()
			data = res.read()
			dic = json.loads(data)
			for ix in range(len(dic['datarange'])):
				list_col = []
				list_col = [dic['datarange'][ix]['date']['strdate'], datetime.strptime(dic['datarange'][ix]['date']['strdate'], '%m/%d/%Y'), dic['datarange'][ix]['price']]
				c.execute('CREATE TABLE IF NOT EXISTS ' + sec + '\
					(Str_Date DATE PRIMARY KEY, Datetime NUMERIC, Price NUMERIC)')
				c.execute('INSERT INTO ' + sec + ' VALUES(?, ?, ?)', list_col)
				conn_sql.commit()
		c.close()
		print('success creating historical data table')

	comment_table(r"C:\users\pkopp\python_diploma\Capstone\dev\database\email_info.db")
	historical_data(r"C:\users\pkopp\python_diploma\Capstone\dev\database\roboinvest.db")


if __name__ == "__main__":
    main()
