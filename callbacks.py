'''all callbacks for the robo investing system are here
Peter Koppelman July 16, 2020'''

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

import sqlite3
import sys
import pandas as pd

from dash.dependencies import Input, Output, State
from dash import no_update
from apps import reference

def login(app):
    '''Login callback'''
    @app.callback(
	  Output('record', 'data'),
	  [Input('login_submit', 'n_clicks'),
	  Input('record', 'value')],
	  [State('email', 'value'),
	  State('password', 'value')]
    )
    def cl_login(n_clicks, cust_info, email, password):
        if not n_clicks:
            return no_update

		# test to see if either login or password is blank
        if email is None or password is None:
            return 'Your email address and password are required'

        # Data was entered into both the login and password fields.
        # Try to open up the database
        try:
            conn = sqlite3.connect(reference.database)
            cursor = conn.cursor()
        except sqlite3.OperationalError:
            print('There was a problem opening up the roboinvest database')
            return

        # Check login table to see if the record exists. If it exists,
        # see if it is for a (C)ustomer, (E)mployee or (A)dministrator
        cursor.execute(
			'SELECT \
				rec_type \
			FROM \
				Login \
			Where email = ? and Password = ?', \
			(email, password))

        try:
            rec_type = cursor.fetchall()[0][0]
        except ValueError:
            return 'There is no record for this email and password combination'

        if rec_type != 'C':
            return 'This id/password combination is not for a client'

		# Get customer data
        cursor.execute( \
			'SELECT DISTINCT\
				CASE \
				when customer_master.Middle_initial is Null \
				then customer_master.First_name || " " || customer_master.Last_name  \
				else customer_master.First_name || " " || customer_master.Middle_initial || \
				" " || customer_master.Last_name \
				END name, \
				account_master.account_number, \
				account_master.account_balance, \
				journal_entries.date_of_entry, \
				journal_entries.transaction_type,\
				journal_entries.transaction_amount \
			FROM \
				customer_master \
				Inner join login On \
					login.id = customer_master.cust_id \
				Inner join account_master On \
					account_master.cust_id = customer_master.cust_Id \
				Inner join journal_entries On \
					journal_entries.cust_id = account_master.cust_id \
				Where \
					login.email = ? and login.password = ?', \
					(email, password))

        customer_information = []
        customer_information = cursor.fetchall()
        cursor.close()

        cust_info = []
        for count, info in enumerate(customer_information):
            cust_info.append([info[0], info[1], info[2], info[3], info[4], info[5]])

		# Create pandas dataframe
        cust_info = pd.DataFrame(cust_info,
            columns = ['name', 'account number', 'account balance', 'date of entry',
                'transaction type', 'transaction amount'])
		# print('cust_info ', cust_info)
		# send cust_info to layout.present_customer_data_layout
        return cust_info.to_dict('records')


def open_account(app):
    '''Open account'''
    @app.callback(
	  Output('open_account_button', 'children'),
	  [Input('account_opening_button', 'n_clicks')],
	  [State('fname', 'value'),
	  State('m_init', 'value'),
	  State('lname', 'value'),
	  State('addr', 'value'),
	  State('city', 'value'),
	  State('st', 'value'),
	  State('zipcode', 'value'),
	  State('email', 'value'),
	  State('tin', 'value'),
	  State('dob', 'value'),
	  State('password', 'value')]
	)
    def enter_data(n_clicks, fname, minit, lname, addr, city, state, zipcode, \
			email, tin, dob, password):

        if not n_clicks:
            return no_update

		# Checking that clients entered the required data
        if [x for x in (fname, lname, addr, city, state, zipcode, email, tin, \
            dob, password) if x is None]:
            return 'The following fields are required: first name, last name, address, \
                city, state, zipcode, email, tax id number, date of birth and password'

		# Passed data validation. Open database and enter information into account master,
        # reference_id and login tables
        try:
            connect = sqlite3.connect(reference.database)
            cursor = connect.cursor()
        except sqlite3.OperationalError:
            print('There was a problem opening up the roboinvest database')
            return

        # Check to see if a record for this client already exists in the customer master table
        cursor.execute(
		'SELECT \
		   * \
		FROM \
		   customer_master \
		Where \
		   First_name =? and Middle_initial IS ? and Last_name = ? and \
		   Street_addr = ? and City = ? and State = ? and Zip_code = ? \
		   and Email_addr = ? and TIN = ? and DOB = ?',\
		   (fname, minit, lname, addr, city, state, zipcode, email, tin, dob))

        data_set = cursor.fetchall()

		# data_set is not Null. There is a record in our database.
        if data_set:
            cursor.close()
            return 'There is already a record in our database for you.'

        # data_set is Null. We didn't find anything. Enter the new record in the table.

        # Add a new record to the customer master file
        datalist = [fname, minit, lname, addr, city, state, zipcode,
        email, tin, dob, datetime.now()]
        cursor.execute('INSERT INTO Customer_Master (First_name, Middle_initial, Last_name, \
			Street_addr, City, State, Zip_code, Email_addr, TIN, DOB, time_stamp) VALUES \
			(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', datalist)
        connect.commit()

		# Get master account number from customer master. It should have been automatically
		# created (autoincrement) when the record was written...
        cursor.execute(
			'SELECT \
				Cust_Id \
			FROM \
				Customer_Master \
			Where \
				First_name = ? and Middle_initial IS ? and Last_name = ? and \
				Street_addr = ? and City = ? and State = ? and Zip_code = ? \
				and Email_addr = ? and TIN = ? and DOB = ?',\
				(fname, minit, lname, addr, city, state, zipcode, email, tin, dob))

        cust_id = []
        cust_id = cursor.fetchall()[0][0]

        # Add new record to account master file.
        # For the moment, account number will be 1 for each account - this is for the MVP
        account_number = 1
        # Account balance is 0 when you open an account.
        account_balance = 0

        datalist = [cust_id, account_number, account_balance, datetime.now()]
        cursor.execute('INSERT INTO account_master VALUES(?, ?, ?, ?)', datalist)
        connect.commit()

        # Create a new record in the login table. Type will be value 'C' for customer
        datalist = [cust_id, email, password, 'C', datetime.now()]
        cursor.execute('INSERT INTO Login VALUES(?, ?, ?, ?, ?)', datalist)
        connect.commit()
        cursor.close()
        return 'Your information has been entered into our system'


def sample_portfolio(app, df_portfolio):
    '''Sample portfolio'''
    @app.callback(
		Output('df_portfolio', 'data'),
		[Input('df_portfolio', 'value'),
		Input('my-age', 'value'),
		Input('my-amount', 'value'),
		Input('risk-tolerance-slider', 'value')]
	)
    def portfolio(sample_portfolio, age, account_bal, risk_tolerance):
		# create portfolio based on age and risk tolerance

        if age is None or account_bal is None:
            return no_update

        try:
            conn = sqlite3.connect(reference.database)
            cursor = conn.cursor()
        except sqlite3.OperationalError:
            print('There was a problem opening up the roboinvest database')
            return

		# Get security information, category and price history
        cursor.execute(
			'SELECT \
				price_history.Sec,\
				price_history.Price, \
				sec_info.Name, \
				sec_info.Category \
			FROM \
				price_history \
			Inner Join sec_info On price_history.Sec = sec_info.ticker and \
				count = (select max(count) from price_history) \
				order by sec_info.rowid')
        sec_val_list = cursor.fetchall()

		# Determine base portfolio from age
        cursor.execute(
			'SELECT \
				base_portfolio, \
				adjustment \
			FROM \
				portfolio_weightings \
			WHERE \
				age_min <= ? and age_max >= ?', \
				(age, age))

        data = cursor.fetchall()
        cursor.close()
        portfolio = data[0][0]
        adjustment = data[0][1]

        portfolio = (portfolio).split(',')
        portfolio = [float(i) for i in portfolio]

        adj_portfolio = []
        # Adjust for risk tolerance.
        if risk_tolerance < 5:
            for count, percent in enumerate(portfolio):
                risk_adjuster = -adjustment if count <= 2 else adjustment
                adj_portfolio.append(percent +
                    (percent * (risk_adjuster/10 * (5 - risk_tolerance))))

        elif risk_tolerance > 5:
            for count, percent in enumerate(portfolio):
                risk_adjuster = adjustment if count <= 1 else -adjustment
                adj_portfolio.append(percent +
                    (percent * (risk_adjuster/10 * (risk_tolerance - 5))))

        else:  # risk_tolerance = 5
            adj_portfolio = portfolio

        # if adj_portfolio does not = 100, adjustments will be off and
        # we will not allocate the entire amount of the portfolio properly.
        # An adjuster is created that is the amount of the difference between
        # adj_portfolio and 100. Each element except cash (which could be 0)
        # in adj_portfolio will get adjusted in an equal percentage based on the
        # delta between the adj_portfolio value and the amount of items in the portfolio
        adj_portfolio2 = []
        if sum(adj_portfolio) != 100:
            # set the adjuster to 4 decimal places to round to 100.
            adjuster = round(100/sum(adj_portfolio), 4)
            for count, value in enumerate(adj_portfolio):
                adj_portfolio2.append(round(value * adjuster, 4))
                # if the adj_portfolio < 0 make it 0. You can't allocate less than
                # 0 part of the portfolio.
                if adj_portfolio2[count] < 0:
                    adj_portfolio2[count] = 0
        else:
            adj_portfolio2 = adj_portfolio


        # Calculate the number of shares of each security that will be purchased.
        # Only full shares can be purchased, not partial ones. For this reason, cash is
        # the amount of money left over after the purchase.
        share_count = []
        cash = account_bal
        count = 0
        for value, share_price in zip(adj_portfolio2, sec_val_list):
            share_count.append(int((account_bal * value/100) / share_price[1]))
            cash -= share_count[count] * share_price[1]
            count +=1

        # round cash to the second decimal place
        cash = round(cash, 2)

        portfolio = []
        for sec_val_list, share_count in zip(sec_val_list, share_count):
            portfolio.append([sec_val_list[2],
                      sec_val_list[3],
                      share_count,
                      sec_val_list[1],
                      share_count * sec_val_list[1]])
        # add cash on at the end of the portfolio list. It appers at the bottom of the datatable.
        portfolio.append(['Cash', 'N/A', 'N/A', 'N/A', cash])

		# Create pandas dataframe of sample portfolio and push out to layout screen.
        sample_portfolio = pd.DataFrame(portfolio,
            columns = ['security', 'category', 'shares', 'share price', 'total cost'])
        return sample_portfolio.to_dict('records')
    return


def contact_layout(app):
    '''Send email to us'''
    @app.callback(
		Output('email_to', 'children'),
		[Input('submit-email', 'n_clicks')],
		[State('name', 'value'),
		State('email-addr', 'value'),
		State('comment', 'value')]
	)
    def send_email(n_clicks, name, email_addr, comment):
        if not n_clicks:
            return no_update

        try:
            conn = sqlite3.connect(reference.database)
            cursor = conn.cursor()
        except sqlite3.OperationalError:
            print('There was a problem opening up the roboinvest database')
            return

        datalist = [name, email_addr, comment, datetime.now()]
        cursor.execute('INSERT INTO `email_info` VALUES(?, ?, ?, ?)', datalist)
        conn.commit()
        cursor.close()

        message = MIMEMultipart('alternative')
        message['Subject'] = 'Email message to the Shore-Koppelman Group'
        message_body = 'An email came from: '+ name+'\n'\
            'At email address: '+ email_addr+'\n' 'Comment: '+ comment
        message.attach(MIMEText(message_body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(reference.account, reference.password)

            # Sent from, sent to, message
            server.sendmail(email_addr, reference.recipients, message.as_string())
            server.quit()
            return '\nThank you, your email has been sent'
        except sqlite3.OperationalError:
            print('Email did not send ')
            return 'Sorry, there was a problem sending your email'


def journal_data_entry(app, cust_info, ee_info, acct_info):
# def journal_data_entry(app):
    '''Journal entry - deposit or withdrawal'''
    @app.callback(
		Output('journal_entry_complete', 'children'),
		[Input('journal_submit_button', 'n_clicks')],
		[State('date_of_entry', 'date'),
		State('customer', 'value'),
		State('acct_number', 'value'),
		State('transaction_amount', 'value'),
		State('transaction_type', 'value'),
		State('ee_lname', 'value'),
		State('ee_tin', 'value'),
		State('ee_dob', 'value')]
	)
    def journal_entry(n_clicks, date_of_entry, customer, acct_number, transaction_amount,
		transaction_type, ee_lname, ee_tin, ee_dob):

        if not n_clicks:
            return no_update

        # def validate_data(transaction_amount, acct_number, ee_tin, ee_dob):
			# test to see if any data is blank
        if transaction_amount is None or acct_number is None or \
			ee_tin is None or ee_dob is None:
            return 'Please make sure that all information is filled in.'

		# Transaction amount cannot be 0
        if transaction_amount is None or transaction_amount < 1:
            return 'The transaction amount must be at least $1.'

        # Data was entered into both the login and password fields.
        # Check for record in Login table
        try:
            conn = sqlite3.connect(reference.database)
            cursor = conn.cursor()
        except sqlite3.OperationalError:
            print('There was a problem opening up the roboinvest database')
            return

		# Check to see if a record for this employee.
		# Only an employee can enter data for a client
        cursor.execute(
			'SELECT \
				ee_id, \
				TIN, \
				DOB \
			FROM \
				Employee_Master \
			Where \
				ee_id = ? and TIN = ? and DOB = ?', \
				(ee_lname, ee_tin, ee_dob))

        data_set = cursor.fetchall()
		# data_set is Null. We didn't find anything. Issue errror message
        if not data_set:
            return 'There is no record for this employee information. Please try again.'

		# We've passed the tests. Write the data to the journal
		# make ticker symbol ' ' as it is not used for this journal entry
        ticker = ' '
        datalist = [date_of_entry, customer, acct_number, transaction_type,
			transaction_amount, ee_lname, ticker, datetime.now()]
        cursor.execute('INSERT INTO journal_entries VALUES(?, ?, ?, ?, ?, ?, ?, ?)', datalist)
        conn.commit()

		# Is this a new account for the master account? if so, write a new record in the
		# account master table. If not, update the applicable record in the account
		# master table.
        cursor.execute( \
			'SELECT \
				cust_id, \
				account_number, \
				account_balance \
			FROM \
				account_master \
			WHERE \
				cust_id = ? and account_number = ?',\
				(customer, acct_number))
        cust_acct = cursor.fetchall()
        current_account_balance = cust_acct[0][2]

		# new record
        if not cust_acct:
            datalist = [customer, acct_number, current_account_balance,
				ee_lname, datetime.now()]
            cursor.execute('INSERT INTO account_master VALUES (?,?,?,?,?)', datalist)
        else:

			# Update account balance in account_master file...
            new_account_balance = current_account_balance - transaction_amount \
            if transaction_type == 'Withdrawal' else \
				current_account_balance + transaction_amount
            datalist = [new_account_balance, customer, acct_number]
            cursor.execute('UPDATE account_master set account_balance = ? \
				WHERE account_master.cust_id = ? and \
				account_master.account_number = ?', datalist)
        conn.commit()

		# Get email data from customer and email them to say that we have their money
        cursor.execute(\
			'SELECT \
				email_addr \
			FROM \
				Customer_Master \
			Inner Join journal_entries On journal_entries.ee_id = Customer_Master.cust_id')
        email = cursor.fetchall()
        email_addr = email[0][0]
        cursor.close()

        message = MIMEMultipart('alternative')
        message['Subject'] = 'Email message from the Shore-Koppelman Group'
        message_body = 'A '+transaction_type+' of '+str(transaction_amount)+' \
        	has been made in your account.'
        message.attach(MIMEText(message_body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(reference.account, reference.password)
            from_addr = 'Roboinvest.com'

            # Sent from, sent to, message
            server.sendmail(from_addr, email_addr, message.as_string())
            server.quit()
            return 'Journal entry completed. An email has been sent to the clients account \
				alerting them that this transaction is complete.'
        except Exception as e:
            print ('email did not send', e)
            return 'There was a problem with our system. Your email did not get sent.'
        return
