# reference.py - this is a reference file with 
# sensitive data for the robo investing system.
# Peter Koppelman - July 12, 2020

import dash_html_components as html
import http.client
import json


# Email Password anc account
password = 'NYUCapstone'
account = 'capstone.roboinvesting@gmail.com'

# Recipients of emails
# recipients = ['pbkoppelman@gmail.com', 'michael.shore93@gmail.com']
recipients = ['pbkoppelman@gmail.com']

# base portfolio -this is a list of lists.
base_portfolio = [[55.,30.0,5.0,5.0,5.0], [50.0,30.0,10.0,5.0,5.0], [45.0,30.0,10.0,10.0,5.0], 
	[45.0,25.0,10.0,10.0,10.0], [40.0,25.0,15.0,10.0,10.0], [40.0,20.0,15.0,15.0,10.0], 
	[35.0,15.0,20.0,20.0,10.0], [30.0,15.0,25.0,20.0,10.0], [25.0,15.0,25.0,20.0,10.0], 
	[25.0,15.0,30.0,25.0,5.0]]


'''for each increase or decrease in the risk tolerance the portfolio will move 2.5% in either a riskier
    direction (more equities) or more conservative (more fixed income). The 2.5% increase in risk will be 
    shared equally by the equity pieces of the portfolio. The 2.5% decrease in risk will be shared 
    equally by the domestic bond peices of the portfolio. PK 6/29/2020'''
adj = .0125


# security list
sec_list = ["VOO", "PRULX", "VTIAX", "PFORX", "FDHY", "SPY"]

# Database connectivity

conn = http.client.HTTPSConnection("ftlightning.fasttrack.net")
# conn.request("GET", "/v1/auth/login?account=300724&pass=1243OEIL&appid=F075C6E1-759C-4009-9B47-5FE284F31F55")
x = 'GET'
y = "/v1/auth/login?account=300724&pass=1243OEIL&appid=F075C6E1-759C-4009-9B47-5FE284F31F55"
conn.request(x,y)
res = conn.getresponse()
data = json.loads(res.read())
appid = data['appid']
token = data['token']

# setting paths and naming database table paths.
db_path = '/users/pkopp/python_diploma/Capstone/dev/apps'
db_email = r"C:\users\pkopp\python_diploma\Capstone\dev\database\email_info.db"
