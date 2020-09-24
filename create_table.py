'''This is the create table program in the roboinvest system. It creates all of the
database tables and populates the securities and historical pricing tables.
Peter Koppelman September 9, 2020.'''
import sqlite3
import http.client
import json
import sys

from datetime import datetime

# sys.path.insert(1, '/roboinvest/apps')
sys.path.insert(1, '/Users/pkopp/python_diploma/capstone/dev/apps')
import reference

def main():
    '''Below are functions to create and populate database tables for the roboinvest system'''

    def comment_table(connect, cursor):
        cursor.execute('CREATE TABLE IF NOT EXISTS Email_Info\
			(Name TEXT, \
			Email_Address TEXT, \
			Comment TEXT, \
			Time_stamp Datetime)')

        connect.commit()

    def login(connect, cursor):
        cursor.execute('CREATE TABLE IF NOT EXISTS Login\
			(cust_id NUMERIC PRIMARY KEY, \
			email Text, \
			Password Text, \
			rec_type Text, \
			Time_stamp Datetime)')

        connect.commit()

    def customer_master(connect, cursor):
        cursor.execute('CREATE TABLE IF NOT EXISTS Customer_Master\
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

        connect.commit()

    def employee_master(connect, cursor):
        cursor.execute('CREATE TABLE IF NOT EXISTS Employee_Master\
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

        connect.commit()

    def account_master(connect, cursor):
        cursor.execute('CREATE TABLE IF NOT EXISTS account_master\
			(cust_id Integer, \
			account_number Integer, \
			account_balance NUMERIC, \
			Time_stamp Datetime, \
			PRIMARY KEY (cust_id, account_number))')

        connect.commit()


    def journal_entry(connect, cursor):
        cursor.execute('CREATE TABLE IF NOT EXISTS journal_entries\
			(Date_of_entry Date, \
				cust_id Integer, \
				account_number TEXT, \
				transaction_type TEXT, \
				transaction_amount NUMERIC, \
				ee_id Integer, \
				ticker_symbol Text, \
				Time_stamp Datetime, \
				PRIMARY KEY (cust_id, account_number,Time_stamp))')
        connect.commit()

    def age_reference_data(connect, cursor):
        cursor.execute('CREATE TABLE IF NOT EXISTS portfolio_weightings \
			(age_min Integer, \
				age_max Integer, \
				base_portfolio Text, \
				adjustment NUMERIC, \
				Time_stamp Datetime)')

        date_time = datetime.now()
        data = [(18, 22, '55.,30.0,5.0,5.0,5.0', 1.0, date_time), \
        	(23, 27, '50.0,30.0,10.0,5.0,5.0', .9, date_time), \
        	(28, 32, '45.0,30.0,10.0,10.0,5.0', .8, date_time), \
        	(32, 37, '45.0,25.0,10.0,10.0,10.0', .7, date_time), \
        	(38, 42, '40.0,25.0,15.0,10.0,10.0', .6, date_time), \
        	(43, 47, '40.0,20.0,15.0,15.0,10.0', .5, date_time), \
        	(48, 52, '35.0,15.0,20.0,20.0,10.0', .4, date_time), \
        	(53, 57, '30.0,15.0,25.0,20.0,10.0', .3, date_time), \
        	(58, 62, '25.0,15.0,25.0,20.0,10.0', .2, date_time), \
        	(63, 99, '25.0,15.0,30.0,25.0,5.0', .1, date_time)]

        cursor.executemany('INSERT INTO portfolio_weightings \
        	(age_min, age_max, base_portfolio, adjustment, Time_stamp) \
        	VALUES (?, ?, ?, ?, ?)', data)

        connect.commit()


    def historical_data(connect, cursor):
        conn_ft = http.client.HTTPSConnection("ftl.fasttrack.net")
        headers = {
        'appid': reference.appid,
        'token': reference.token
        }
        # Get historical data - daily price closing history
        for sec in reference.sec_list:
            conn_ft.request("GET", "/v1/data/" + sec + "/range?start=1%2F1%2F2000&adj=&olhv=0",
                headers=headers)
            res = conn_ft.getresponse()
            data = res.read()
            dic = json.loads(data)
            count = 1
            for counter in range(len(dic['datarange'])):
                list_col = []
                list_col.append(dic['datarange'][counter]['date']['strdate'])
                list_col.append(sec)
                list_col.append(dic['datarange'][counter]['price'])
                list_col.append(count)
                list_col.append(datetime.now())

                cursor.execute('CREATE TABLE IF NOT EXISTS price_history \
                	(As_of_Date DATE NOT NULL, \
                	Sec TEXT NOT NULL, \
                	Price Numeric NOT NULL, \
                	Count Integer NOT NULL, \
                	Time_stamp Datetime, \
                	Unique(As_of_Date, Sec, Price, Count))')
                cursor.execute('INSERT INTO price_history VALUES (?, ?, ?, ?, ?)', list_col)
                count += 1
                connect.commit()

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

            cursor.execute('CREATE TABLE IF NOT EXISTS Sec_Info \
        		(Ticker String PRIMARY KEY, \
        		Name String NOT Null, \
        		Category String NOT Null, \
        		Time_stamp Datetime Not Null)')
            try:
                cursor.execute('INSERT INTO Sec_Info VALUES(?, ?, ?, ?)', list_col)
            except sqlite3.OperationalError:
                print('Unable to insert data into security info table.')
            connect.commit()


    ##### start running code #####
    # Create connection to sqlite3
    connect = sqlite3.connect(reference.database)
    cursor = connect.cursor()

    # Create datbase tables
    # comment_table(reference.database, conn, c)
    comment_table(connect, cursor)
    print('success creating comment table')
    # login(reference.database, conn, c)
    login(connect, cursor)
    print('Success creating login table')
    # customer_master(reference.database, conn, c)
    customer_master(connect, cursor)
    print('Success creating customer master table')
    # employee_master(reference.database, conn, c)
    employee_master(connect, cursor)
    print('Success creating employee master table')
    # account_master(reference.database, conn, c)
    account_master(connect, cursor)
    print('Success creating account master table')
    # journal_entry(reference.database, conn, c)
    journal_entry(connect, cursor)
    print('Success creating journal entry table')
    # age_reference_data(reference.database, conn, c)
    age_reference_data(connect, cursor)
    print('Success creating and populating age reference data table')
    # historical_data(reference.database, conn, c)
    historical_data(connect, cursor)
    print('Success creating and populating historical data table')

    # Close connection to database
    connect.close()


if __name__ == "__main__":
    main()
