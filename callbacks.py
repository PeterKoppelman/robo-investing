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
      Output('intl_bonds', 'children')],
      [Input('my-age', 'value'),
      Input('risk-tolerance-slider', 'value'),
      Input('my-amount', 'value')]
   )

   def portfolio(age, risk_tolerance, amount):
      # create portfolio based on age and risk tolerance
      # first item in each list is the percentage of the portolio in the following:
      # 1) domestic equity
      # 2) international equity
      # 3) domestic government bonds
      # 4) domestic corporate bonds
      # 5) international bonds.
      # Each list is for a group 20, 25,30, 35, 40, etc up to 65
      account_bal = amount
      #  # portfolio = [0.25, 0.1, 0.3, 0.1, 0.25]
      conn = http.client.HTTPSConnection("ftlightning.fasttrack.net")

      conn.request("GET", "/v1/auth/login?account=300724&pass=1243OEIL&appid=F075C6E1-759C-4009-9B47-5FE284F31F55")

      res = conn.getresponse()
      data = json.loads(res.read())

      appid = data['appid']
      token = data['token']
      # print(data)

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

      # The base portfolio is used when the risk tolerance is 5 (neutral)  
      # For positions 0 - 4 see above.
      # base_portfolio = [[55,30,5,5,5], [50,30,10,5,5], [45,30,10,10,5], [45,25,10,10,10], [40,25,15,10,10],
      #    [40,20,15,15,10], [35,15,20,20,10], [30,15,25,20,10], [25,15,25,20,10], [25,15,30,25,5]]


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

      # for each increase or decrease in the risk tolerance the portfolio will move 2.5% in either a riskier
      # direction (more equities) or more conservative (more fixed income). The 2.5% increase in risk will be 
      # shared equally by the equity pieces of the portfolio. The 2.5% decrease in risk will be shared 
      # equally by the domestic bond peices of the portfolio. PK 6/29/2020
      # adj = .0125

      if risk_tolerance < 5:
         portfolio[0] += portfolio[0] * (-reference.adj * (5 - risk_tolerance))
         portfolio[1] += portfolio[1] * (-reference.adj * (5 - risk_tolerance))
         portfolio[2] += portfolio[2] * (reference.adj * (5 - risk_tolerance))
         portfolio[3] += portfolio[3] * (reference.adj * (5 - risk_tolerance))
         portfolio[4] += portfolio[4] * (reference.adj * (5 - risk_tolerance))
      elif risk_tolerance > 5:
         portfolio[0] += portfolio[0] * (reference.adj * (risk_tolerance - 5))
         portfolio[1] += portfolio[1] * (reference.adj * (risk_tolerance - 5))
         portfolio[2] += portfolio[2] * (-reference.adj * (risk_tolerance - 5))
         portfolio[3] += portfolio[3] * (-reference.adj * (risk_tolerance - 5))
         portfolio[4] += portfolio[4] * (-reference.adj * (risk_tolerance - 5))


      dom_stock  = int((account_bal * portfolio[0]) / sec_val_list[0])
      dom_stock_rem = portfolio[0] * account_bal - (dom_stock * sec_val_list[0])
      gov_bond  = int((account_bal * portfolio[1]) / sec_val_list[1])
      gov_bond_rem = portfolio[1] * account_bal - (gov_bond * sec_val_list[1])
      int_stock  = int((account_bal * portfolio[2]) / sec_val_list[2])
      int_stock_rem = portfolio[2] * account_bal - (int_stock * sec_val_list[2])
      int_bond  = int((account_bal * portfolio[3]) / sec_val_list[3])
      int_bond_rem = portfolio[3] * account_bal - (int_bond * sec_val_list[3])
      corp_bond  = int(account_bal * portfolio[4] / sec_val_list[4])
      corp_bond_rem = portfolio[4] * account_bal - (corp_bond * sec_val_list[4])
      ttl_rem = dom_stock_rem + gov_bond_rem + int_stock_rem + int_bond_rem + corp_bond_rem
      rem_spy = ttl_rem / sec_val_list[5]


      return ('${:,.2f}'.format(portfolio[0]/100 * amount), 
         '${:,.2f}'.format(portfolio[1]/100 * amount), 
         '${:,.2f}'.format(portfolio[2]/100 * amount), 
         '${:,.2f}'.format(portfolio[3]/100 * amount), 
         '${:,.2f}'.format(portfolio[4]/100 * amount))
