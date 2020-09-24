# reference.py - this is a reference file with 
# sensitive data for the robo investing system.
# Peter Koppelman - July 12, 2020

import dash_html_components as html
import http.client
import json


# Email Password and account. Please set up your own...
password = 
account = 

# Recipients of emails. Create as a list
recipients = []

# Database connectivity to fastrack
conn = http.client.HTTPSConnection("ftlightning.fasttrack.net")
x = 'GET'
y is account informaiton from fasttrack
conn.request(x,y)
res = conn.getresponse()
data = json.loads(res.read())
appid = data['appid']
token = data['token']

# list of securiities in the portfolio. We want their call symbols
sec_list = []

# setting paths and naming database table paths.
db_path = '/roboinvest/apps'
database = r"C:\roboinvest\database\roboinvest.db"
