# all callbacks are here
from dash.dependencies import Input, Output, State

import http.client
import json

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email_to

from apps import reference

def contact_callback(app):
	@app.callback(
		[Output('counter', 'children')],
		[Input('submit-email', 'n_clicks')],
		[State('name', 'value'),
		State('email-addr', 'value'),
		State('comment', 'value')]
	)
	def send_email(n, name, email_addr, comment):
   		if n > 0:
   			message = MIMEMultipart('alternative')
   			message['Subject'] = 'Email message to the Shore-Koppelman Group'
   			message_body = 'An email came from: '+ name+'\n' 'At email address: '+ email_addr+'\n' 'Comment: '+ comment
   			message.attach(MIMEText(message_body, 'plain'))

   			try:
   				server = smtplib.SMTP('smtp.gmail.com', 587)
   				server.starttls()
   				# server.login('pbkoppelman@gmail.com', password)
   				server.login(reference.account, reference.password)


   				# Sent from, sent to, message
   				# server.sendmail(email_addr, 'pbkoppelman@gmail.com', message.as_string())
   				server.sendmail(email_addr, reference.recipients, message.as_string())
   				server.quit()
   				return [f'\nThank you, your email has been sent']
   			except Exception as e:
   				print('email did not send ', e)
   				return[f'Sorry, there was a problem sending your email']
   		else:
   			return ['']


def sample_portfolio_callback(app):
   @app.callback(
      [Output('domestic_equity', 'children'),
      Output('intl_equity', 'children'),
      Output('govy_bonds', 'children'),
      Output('corp_bonds', 'children'),
      Output('intl_bonds', 'children'),
      Output('cash', 'children')],
      [Input('my-age', 'value'),
      Input('risk-tolerance-slider', 'value'),
      Input('my-amount', 'value')]
   )

   def portfolio(age, risk_tolerance, account_bal):
      # create portfolio based on age and risk tolerance
      # first item in each list is the percentage of the portolio in the following:
      # 1) domestic equity
      # 2) international equity
      # 3) domestic government bonds
      # 4) domestic corporate bonds
      # 5) international bonds.
      # Each list is for a group 20, 25,30, 35, 40, etc up to 65

      # For some reason when typing in a new value for age or account_bal we get a Nonetype error.
      # This prevents the error.
      if age is None or account_bal is None:
         return ['','','','','','']

      conn = http.client.HTTPSConnection("ftlightning.fasttrack.net")
      conn.request("GET", "/v1/auth/login?account=300724&pass=1243OEIL&appid=F075C6E1-759C-4009-9B47-5FE284F31F55")

      res = conn.getresponse()
      data = json.loads(res.read())

      appid = data['appid']
      token = data['token']

      headers = {'appid': appid,
                  'token': token}
 
      sec_list = ["VOO", "PRULX", "VTIAX", "PFORX", "FDHY", "SPY"]
      sec_val_list = []

      for sec in sec_list:
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
      adj_portfolio = [0] * len(sec_list)
    
      # Adjust for risk tolerance.
      if risk_tolerance < 5:
         for i in range(len(adj_portfolio) - 1):
            if i <= 2:
               adj_portfolio[i] = portfolio[i] + (portfolio[i] * (-reference.adj * (5 - risk_tolerance)))
            else:
               adj_portfolio[i] = portfolio[i] + (portfolio[i] * (reference.adj * (5 - risk_tolerance)))
      elif risk_tolerance > 5:
         for i in range(len(adj_portfolio) - 1):
            if i <= 1:
               adj_portfolio[i] = portfolio[i] + (portfolio[i] * (reference.adj * (risk_tolerance - 5)))
            else:
               adj_portfolio[i] = portfolio[i] + (portfolio[i] * (-reference.adj * (risk_tolerance - 5)))
      else:        # risk_tolerance = 5
         adj_portfolio = portfolio

      # Number of sharees of each security.
      dom_stock  = int((account_bal * adj_portfolio[0]/100) / sec_val_list[0])
      gov_bond  = int((account_bal * adj_portfolio[1]/100) / sec_val_list[1])
      int_stock  = int((account_bal * adj_portfolio[2]/100) / sec_val_list[2])
      int_bond  = int((account_bal * adj_portfolio[3]/100) / sec_val_list[3])
      corp_bond  = int(account_bal * adj_portfolio[4]/100 / sec_val_list[4])
      cash = account_bal - ((dom_stock * sec_val_list[0]) + (gov_bond * sec_val_list[1]) + 
         (int_stock * sec_val_list[2]) + (int_bond * sec_val_list[3]) + (corp_bond * sec_val_list[4]))


      return ('{} shares at ${:,.2f} per share or ${:,.2f}'.format(dom_stock, sec_val_list[0], dom_stock * sec_val_list[0]),
      '{} shares at ${:,.2f} per share or ${:,.2f}'.format(gov_bond, sec_val_list[1], gov_bond * sec_val_list[1]),
      '{} shares at ${:,.2f} per share or ${:,.2f}'.format(int_stock, sec_val_list[2], int_stock * sec_val_list[2]),
      '{} shares at ${:,.2f} per share or ${:,.2f}'.format(int_bond, sec_val_list[3], int_bond * sec_val_list[3]),
      '{} shares at ${:,.2f} per share or ${:,.2f}'.format(corp_bond, sec_val_list[4], corp_bond * sec_val_list[4]),
      '${:,.2f}'.format(cash))
