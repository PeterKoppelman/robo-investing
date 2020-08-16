# all callbacks for the robo investing system are here
# Peter Koppelman July 16, 2020
from dash.dependencies import Input, Output, State
from dash import no_update
from dash.exceptions import PreventUpdate


import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import http.client
import pandas as pd
import json

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# import email_to

from apps import reference, layout

from datetime import datetime
from sqlalchemy import Column, Date, String, create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3

# import string library function  
import string 

import sys
# sys.path.insert(1, '/roboinvest/apps')



def present_customer_detail(app):
   @app.callback(
      Output('client_detail', 'children'),
      [Input('is_client', 'children'),
      Input('acct_num', 'value')]
   )
   def get_journal_detail(is_client, acct_num):
      print('in get journal detail')
      print('acct num = ', acct_num)
      # if input is_client is not true, exit. There is no client data to get.
      if is_client is not True:
         return

      c.execute( \
         'SELECT \
            Date_of_entry, \
            Debit_amount, \
            Credit_amount, \
            Description, \
         FROM \
            journal_entries \
         Where \
            master_acount_id = ?', \
            (acct_num))
      journal_entries = c.fetchall()
      print('journal entries = ',journal_entries)
      return journal_entries


def present_customer_data(app):
   @app.callback(
      Output('is_client', 'children'),
      [Input('is_client', 'data-valid')],
      [State('client_lname', 'value'),
      State('client_tin', 'value'),
      State('client_dob', 'value'),
      State('acct_num', 'value')]
   )
   # def get_client_data(is_client, client_lname, client_tin, client_dob):
   def get_client_data(is_client, client_lname, client_tin, client_dob, acct_num):
      # if is_client is True we have a client match. 
      # Else it is false and print applicable error message from client_login function
      if is_client is not True:
         return is_client

      # Open sql engine
      engine = create_engine('sqlite:///roboinvest.db')
      Base = declarative_base()
      conn = sqlite3.connect(reference.database)
      c = conn.cursor()

      # check to see of the customer has set up an account yet
      c.execute( \
         'SELECT \
            *\
         FROM \
         account_master \
         Inner Join customer_master On customer_master.cust_id = account_master.master_account_id')

      account_info = c.fetchall()
      if account_info is None:
         return "I'm sorry, an account has not been set up for this customer yet"

      # Check to see if money has been deposited into the journal entry table
      c.execute( \
         'SELECT \
         * \
         FROM \
         journal_entries \
         Inner Join customer_master On customer_master.cust_id = journal_entries.cust_id')
      journal_entries = c.fetchall()
      if journal_entries is None:
         return "I'm sorry, no money has been deposited with us yet"

      # Get data to display
      c.execute( \
         'SELECT DISTINCT\
            CASE \
               when customer_master.Middle_initial is Null \
               then customer_master.First_name || " " || customer_master.Last_name  \
               else customer_master.First_name || " " || customer_master.Middle_initial || " " || customer_master.Last_name \
            END name, \
            account_master.account_number, \
            account_master.account_balance, \
            CASE \
               when journal_entries.Debit_amount != 0 \
               then journal_entries.Debit_amount \
               else journal_entries.Credit_amount \
            END last_transaction \
         FROM \
            customer_master \
            Inner join account_master On \
               account_master.master_account_id = customer_master.Cust_Id \
            Inner join journal_entries On \
               journal_entries.master_account_id = account_master.master_account_id \
            Where \
               customer_master.Last_name = ? and customer_master.TIN = ? and \
               customer_master.DOB = ?', \
               (client_lname, client_tin, client_dob))

      customer_information = []
      customer_information = c.fetchall()
      # returned value is tuple in a list. This removes the tuple.
      customer_information = [item for sublist in customer_information for item in sublist]

      return layout.present_customer_data_layout(customer_information[0], customer_information[1], 
                     customer_information[2], customer_information[3])


def client_login(app):
   @app.callback(
      Output('is_client', 'data-valid'),
      [Input('login_button', 'n_clicks')], 
      [State('client_lname', 'value'),
      State('client_tin', 'value'),
      State('client_dob', 'value'),
      State('acct_num', 'value')]
   )
   def cl_login(n, client_lname, client_tin, client_dob, acct_num):
      def validate_data(client_lname, client_tin, client_dob):
         # test to see if either login or password is blank
         if client_lname is None or client_tin is None or client_dob is None:
            return False
         else:
            return True 

      # Check to make sure all required fields are entered 
      # (see def validate_data above)
      if n > 0:
         data_ok = validate_data(client_lname, client_tin, client_dob)
         if not data_ok:
            # return 'Your Last Name, TIN and DOB are required'
            return 'Your Last Name, TIN and DOB are required'

         # Data was entered into both the login and password fields. 
         # Check for record in Login table
         engine = create_engine('sqlite:///roboinvest.db')
         Base = declarative_base()
         conn = sqlite3.connect(reference.database)
         c = conn.cursor()
    
         # Check to see if this is a client - use customer master file.
         c.execute(
            'SELECT \
               * \
            FROM \
               Customer_Master \
            Where \
               Last_name = ? and TIN = ? and DOB = ?', \
               (client_lname, client_tin, client_dob))

         data_set = c.fetchall()

         # if nothing was returned there is no record for this person and they are not a client
         if not data_set:
            return "I'm sorry, there is no record for this person"
         # Return True and look for transactional data from client in
         # present_customer_data (above)
         return True

      # this return is just here so that Dash does not produce an error. 
      return no_update


def open_account(app):
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
   def enter_data(n, fname, minit, lname, addr, city, st, zipcode, email, tin, dob, password):

      # Checking that clients entered the required data
      def validate_data(fname, lname, addr, city, st, zipcode, email, tin, dob, password):
         if fname is None or lname is None or addr is None or city is None \
            or st is None or zipcode is None or email is None or tin is None or dob is None \
            or password is None:
            return False
         else:
            return True 

      # Check to make sure all required fields are entered (see def validate_data above)
      if n >= 1:
         data_ok = validate_data \
            (fname, lname, addr, city, st, zipcode, email, tin, dob, password)
         if not data_ok:
            return[f'The following fields are required: first name, last name, address, city, state, zipcode, email, tax id number, date of birth and password']


         # Passed data validation. Open database and enter information into account master,
         # reference_id and login tables
         engine = create_engine('sqlite:///roboinvest.db')
         Base = declarative_base()
         conn = sqlite3.connect(reference.database)
         c = conn.cursor()
    
         # Check to see if a record for this client already exists in the customer master table
         c.execute(
            'SELECT \
               * \
            FROM \
               customer_master \
            Where \
               First_name =? and Middle_initial = ? and Last_name = ? and \
               Street_addr = ? and City = ? and State = ? and Zip_code = ? \
               and Email_addr = ? and TIN = ? and DOB = ?',\
               (fname, minit, lname, addr, city, st, zipcode, email, tin, dob))

         data_set = c.fetchall()
         # data_set is Null. We didn't find anything. Enter the new record in the table.
         if not data_set:
            # Get Id number from reference table. Increment it by 1. This will be the 
            # reference id for the client.
            c.execute('SELECT \
                           * \
                        FROM \
                           reference_id')
            ref_id = []
            ref_id = c.fetchall()

            # result set re_id is a tuple in a list. Make it an integer
            # and add one to it so that the next record has a unique id
            ref_id = ref_id[0][0] + 1
            new_ref_id = [ref_id, datetime.now()]
            time_stamp = datetime.now()

            # Getting database is locked error. 
            # Closing database and re-opening database to try and avoid this.
            c.close()
            engine = create_engine('sqlite:///roboinvest.db')
            Base = declarative_base()
            conn = sqlite3.connect(reference.database)
            c = conn.cursor()

            # Add a new record to the customer master file
            datalist = [ref_id, fname, minit, lname, addr, city, st, zipcode, 
               email, tin, dob, time_stamp]
            c.execute('INSERT INTO `customer_master` VALUES(?, ?, ?, ?, ?, ?, ?,\
               ?, ?, ?, ?, ?)', datalist)
            conn.commit()

            # Add new record to account master file.
            # For the moment, account number will be 1 for each account - this is for the MVP
            account_number = 1
            # Account balance is 0 when you open an account.
            account_balance = 0

            datalist = [ref_id, account_number, account_balance, ref_id, time_stamp]
            c.execute('INSERT INTO `account_master` VALUES(?, ?, ?, ?, ?)', datalist)
            conn.commit()

            # update id and date/time stamp in reference table
            c.execute('UPDATE `reference_id` SET ID = ?, Time_stamp = ?', (new_ref_id))
            conn.commit()
            # Create a new record in the login table. Type will be value 'C' for customer
            datalist = [ref_id, email, password, 'C', time_stamp ]
            c.execute('INSERT INTO `Login` VALUES(?, ?, ?, ?, ?)', datalist)
            conn.commit()
            c.close()
            return[f'Your information has been entered into our system'] 
         else:
            c.close()
            return[f'There is already a record in our database for you.']


def sample_portfolio(app, df_portfolio):
   @app.callback(
      Output('df_portfolio', 'data'),
      [Input('df_portfolio', 'value'),
      Input('my-age', 'value'),
      Input('my-amount', 'value'),
      Input('risk-tolerance-slider', 'value')]
   )

   def portfolio(sample_portfolio, age, account_bal, risk_tolerance):
      '''create portfolio based on age and risk tolerance
      first item in each list is the percentage of the portolio in the following:
      1) domestic equity
      2) international equity
      3) domestic government bonds
      4) domestic corporate bonds
      5) international bonds.
      6) Cash'''

      # For some reason when typing in a new value for age or account_bal we get a Nonetype error.
      # This prevents the error.
      if age is None or account_bal is None:
         return [' '] * len(reference.sec_list)

      conn = None
      try:
         conn = sqlite3.connect('/roboinvest/database/roboinvest.db')
         c = conn.cursor()
      except Error as e:
         print('There are problems opening up the roboinvest database ', e)
         return

      # Get security information, category and price history
      c.execute(
         'SELECT \
            price_history.Sec,\
            price_history.Price, \
            sec_info.Name, \
            sec_info.Category \
         FROM \
            price_history \
         Inner Join sec_info On price_history.Sec = sec_info.ticker and \
            count = (select max(count) from price_history)')

      sec_val_list = []
      sec_val_list = c.fetchall()
      c.close()


      # Determine base portfolio from age
      if (age >= 18 and age <= 22):
         portolio = reference.base_portfolio[0]
      elif (age >= 23 and age <= 27):
         portfolio = reference.base_portfolio[1]
      elif (age >= 28 and age <= 32):
         portfolio = reference.base_portfolio[2]
      elif (age >= 33 and age <= 37):
         portfolio = reference.base_portfolio[3]
      elif (age >= 38 and age <= 42):
         portfolio = reference.base_portfolio[4]
      elif (age >= 43 and age <= 47):
         portfolio = reference.base_portfolio[5]
      elif (age >= 48 and age <= 52):
         portfolio = reference.base_portfolio[6]
      elif (age >= 53 and age <= 57):
         portfolio = reference.base_portfolio[7]
      elif (age >= 58 and age <= 62):
         portfolio = reference.base_portfolio[8]
      else:
         portfolio = reference.base_portfolio[9]

      # initialize adj_portfolio
      adj_portfolio = [0] * len(reference.sec_list)
    
      # Adjust for risk tolerance.
      if risk_tolerance < 5:
         for i in range(len(adj_portfolio) - 1):
            risk_adjuster = -reference.adj if i<= 2 else reference.adj
            adj_portfolio[i] = portfolio[i] + (portfolio[i] * (risk_adjuster * (5 - risk_tolerance)))

      elif risk_tolerance > 5:
         for i in range(len(adj_portfolio) - 1):
            risk_adjuster = reference.adj if i<= 1 else -reference.adj
            adj_portfolio[i] = portfolio[i] + (portfolio[i] * (risk_adjuster * (risk_tolerance - 5)))

      else:        # risk_tolerance = 5
         adj_portfolio = portfolio

      ''' if adj_portfolio does not = 100, adjustments will be off and 
      we will not allocate the entire amount of the portfolio properly.
      An adjuster is created that is the amount of the difference between
      adj_portfolio and 100. Each element except cash (which could be 0)
      in adj_portfolio will get adjusted in an equal percentage based on the
      delta between the adj_portfolio value and the amount of items in the portfolio.
      '''

      if sum(adj_portfolio) != 100:
         adjuster = (sum(adj_portfolio) - 100)/(len(adj_portfolio) - 1)
         for n in range(len(adj_portfolio) - 1):
            adj_portfolio[n] = adj_portfolio[n] - adjuster


      '''Calculate the number of shares of each security that will be purchased.
      Only full shares can be purchased, not partial ones. For this reason, cash is 
      the amount of money left over after the purchase.
      ''' 
      share_count = []
      cash = account_bal
      for count in range(len(adj_portfolio)):
         share_count.append(int((account_bal * adj_portfolio[count]/100) / sec_val_list[count][1]))
         cash -= share_count[count] * sec_val_list[count][1]

      # put the portfolio together - this is a list in a list
      portfolio = []
      for count in range(len(adj_portfolio)):
         portfolio += [[sec_val_list[count][2], 
                     sec_val_list[count][3],
                     share_count[count], 
                     sec_val_list[count][1], 
                     share_count[count] * sec_val_list[count][1]]]
      # add cash on at the end of the portfolio list. It appers at the bottom of the datatable.
      portfolio += [['Cash', 'N/A', 'N/A', 'N/A', cash]]

      # Create pandas dataframe of sample portfolio and push out to layout screen. 
      sample_portfolio = pd.DataFrame(portfolio, 
         columns = ['security', 'category', 'shares', 'share price', 'total cost'])
      return sample_portfolio.to_dict('records')


def contact_layout(app):
   @app.callback(
      Output('email_to', 'children'),
      [Input('submit-email', 'n_clicks')],
      [State('name', 'value'),
      State('email-addr', 'value'),
      State('comment', 'value')]
   )
   def send_email(n, name, email_addr, comment):
      if n > 0:
         engine = create_engine('sqlite:///roboinvest.db')
         Base = declarative_base()
         conn = sqlite3.connect(reference.database)
         c = conn.cursor()

         time_stamp = datetime.now()

         datalist = [name, email_addr, comment, time_stamp]
         c.execute('INSERT INTO `email_info` VALUES(?, ?, ?, ?)', datalist)
         conn.commit()
         c.close()

         message = MIMEMultipart('alternative')
         message['Subject'] = 'Email message to the Shore-Koppelman Group'
         message_body = 'An email came from: '+ name+'\n' 'At email address: '+ email_addr+'\n' 'Comment: '+ comment
         message.attach(MIMEText(message_body, 'plain'))

         try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(reference.account, reference.password)

            # Sent from, sent to, message
            server.sendmail(email_addr, reference.recipients, message.as_string())
            server.quit()
            return [f'\nThank you, your email has been sent']
         except Exception as e:
            print('email did not send ', e)
            return[f'Sorry, there was a problem sending your email']
      else:
         return ['']


def journal_data_entry(app):
   @app.callback(
      Output('journal_entry_complete', 'children'),
      [Input('journal_submit_button', 'n_clicks')], 
      [State('date_of_entry', 'value'),
      State('master_account_number', 'value'),
      State('acct_number', 'value'),
      State('debit_amt', 'value'),
      State('credit_amt', 'value'),
      State('description', 'value'),
      State('ee_lname', 'value'),
      State('ee_tin', 'value'),
      State('ee_dob', 'value')]
   )
   def journal_entry(n, master_account_number, date_of_entry, acct_number, debit_amt, credit_amt, 
      description, ee_lname, ee_tin, ee_dob):
      def validate_data(master_account_number, date_of_entry, acct_number,
         description, ee_lname, ee_tin, ee_dob):
         # test to see if any data is blank
         if master_account_number is None or date_of_entry is None or acct_number is None \
            or description is None or ee_lname is None or ee_tin is None or ee_dob is None:
            return False
         else:
            return True 

      # Check to make sure all required fields are entered 
      # (see def validate_data above)
      if n >= 1:
         data_ok = validate_data(master_account_number, date_of_entry, acct_number,
         description, ee_lname, ee_tin, ee_dob)
         if not data_ok:
            return[f'Some of the critical information is blank. Please make sure that all fields are filled in']

         # Data check for debit and credit...they cannot both be 0 or both be nonzero.
         if debit_amt is None and credit_amt is None:
             return[f'Credit or debit amount must be greater than 0.']
         if debit_amt is not None and credit_amt is not None:
            return[f'Both the credit or debit amount cannot be greater than 0.']
         # Data was entered into both the login and password fields. 
         # Check for record in Login table
         engine = create_engine('sqlite:///roboinvest.db')
         Base = declarative_base()
         conn = sqlite3.connect(reference.database)
         c = conn.cursor()
    
         # Check to see if a record for this employee. Only an employee can enter data for a client
         c.execute(
            'SELECT \
               * \
            FROM \
               Employee_Master \
            Where \
               Last_name = ? and TIN = ? and DOB = ?', \
               (ee_lname, ee_tin, ee_dob))

         data_set = c.fetchall()
         # data_set is Null. We didn't find anything. Issue errror message
         if not data_set:
            return 'There is no record for this employee information. Please try again.'
         user_id = data_set[0][0]

         # Get cust_id from customer_master table.
         c.execute(\
            'SELECT \
               cust_id \
            FROM \
               customer_master \
            Where \
               \
               cust_id = ?', \
               (master_account_number))

         cust_id = c.fetchall()
         if not cust_id:
            return 'There is no record for this customer master id'
         cust_id = cust_id[0][0]

         # We've passed the tests. Write the data to the journal
         time_stamp = datetime.now()
         datalist = [date_of_entry, master_account_number, cust_id, acct_number, 
            debit_amt, credit_amt, description, user_id, ' ', time_stamp]
         c.execute('INSERT INTO `journal_entries` VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', datalist)
         conn.commit()
         # Update account balance in account_master file...
         if credit_amt > 0:
            datalist = [credit_amt, master_account_number, acct_number]
            c.execute('UPDATE `account_master` set account_balance = account_balance + ? \
            WHERE account_master.master_account_id = ? and \
               account_master.account_number = ?', datalist)
         else:
            datalist = [debit_amt, master_account_number, acct_number]
            c.execute('UPDATE `account_master` set account_balance = account_balance - ? \
            WHERE account_master.master_account_id = ? and \
               account_master.account_number = ?', datalist)
         conn.commit()

         # Get email data from customer and email them to say that we have their money
         c.execute(\
            'SELECT \
               email_addr \
            FROM \
               Customer_Master \
            Inner Join journal_entries On journal_entries.ee_id = Customer_Master.cust_id')
         email = c.fetchall()
         email_addr = email[0][0]

         transaction_amt = credit_amt if credit_amt > 0 else debit_amt
         message = MIMEMultipart('alternative')
         message['Subject'] = 'Email message from the Shore-Koppelman Group'
         message_body = 'A transaction of '+str(transaction_amt)+' has been made in your account.'
         message.attach(MIMEText(message_body, 'plain'))

         try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(reference.account, reference.password)
            from_addr = 'Roboinvest.com'

            # Sent from, sent to, message
            server.sendmail(from_addr, email_addr, message.as_string())
            server.quit()
            return 'Journal entry completed. An email has been sent to the clients account alerting them that this transaction is complete.'
         except Exception as e:
            print(f'email did not send ', e)
            return['']
      # else:
      #    return 'Journal entry completed'

