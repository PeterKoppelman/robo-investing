# all callbacks for the robo investing system are here
# Peter Koppelman July 16, 2020
from dash.dependencies import Input, Output, State

import http.client
import pandas as pd
import json

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# import email_to

from apps import reference

from datetime import datetime
from sqlalchemy import Column, Date, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3

import sys
sys.path.insert(1, '/users/pkopp/python_diploma/Capstone/dev/apps')
import reference


def login(app):
   @app.callback(
      Output('login_to_account', 'children'),
      [Input('login_button', 'n_clicks')], 
      [State('login_id', 'value'),
      State('password', 'value')]
   )

   def customer_login(n, login_id, password):
      return[f'thank you'] if n > 0 else ['']

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
      State('dob', 'value')]
   )
   def enter_data(n, fname, minit, lname, addr, city, st, zipcode, email, tin, dob):
      return[f'Your information has been entered into our system'] if n > 0 else ['']


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

      conn = reference.conn
      conn.request(reference.x, reference.y)
      res = conn.getresponse()
      data = json.loads(res.read())
      appid = data['appid']
      token = data['token']
      headers = {'appid': appid,
                  'token': token}


      sec_val_list = []
      for sec in reference.sec_list:
         conn.request("GET", "/v1/data/" + sec + "/divadjprices", headers=headers)
         res = conn.getresponse()
         data = res.read()
         dic = json.loads(data)
         sec_val_list.append(dic["prices"][-1])


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
      the amount of money left over after the purchase''' 
      dom_stock  = int((account_bal * adj_portfolio[0]/100) / sec_val_list[0])
      gov_bond  = int((account_bal * adj_portfolio[1]/100) / sec_val_list[1])
      int_stock  = int((account_bal * adj_portfolio[2]/100) / sec_val_list[2])
      int_bond  = int((account_bal * adj_portfolio[3]/100) / sec_val_list[3])
      corp_bond  = int(account_bal * adj_portfolio[4]/100 / sec_val_list[4])
      cash = account_bal - ((dom_stock * sec_val_list[0]) + (gov_bond * sec_val_list[1]) + 
         (int_stock * sec_val_list[2]) + (int_bond * sec_val_list[3]) + (corp_bond * sec_val_list[4]))

      portfolio = [['Domestic Stock', dom_stock, sec_val_list[0], dom_stock * sec_val_list[0]], 
            ['Govenment Bonds', gov_bond, sec_val_list[1], gov_bond * sec_val_list[1]], 
            ['International Stock', int_stock, sec_val_list[2], int_stock * sec_val_list[2]], 
            ['International Bonds', int_bond, sec_val_list[3], int_bond * sec_val_list[3]],
            ['Corporate Bonds', corp_bond, sec_val_list[4], corp_bond * sec_val_list[4]],
            ['Cash', 'N/A', 'N/A', cash]]

      sample_portfolio = pd.DataFrame(portfolio, columns = ['sector', 'shares', 'share price', 'total cost'])
      return sample_portfolio.to_dict('records')


def contact(app):
   @app.callback(
      [Output('email_to_recepients', 'children')],
      [Input('submit-email', 'n_clicks')],
      [State('name', 'value'),
      State('email-addr', 'value'),
      State('comment', 'value')]
   )
   def send_email(n, name, email_addr, comment):
         if n > 0:
            engine = create_engine('sqlite:///stocks.db')
            Base = declarative_base()
            conn = sqlite3.connect(reference.db_email)
            c = conn.cursor()

            now = str(datetime.now()).replace(':', '-').replace(' ', '-').replace('.', '-')
            timestamp = datetime.now()

            datalist = [now, timestamp, email_addr, comment, name]
            c.execute('INSERT INTO `email_info` VALUES(?, ?, ?, ?, ?)', datalist)
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
