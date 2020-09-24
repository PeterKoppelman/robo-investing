# reference.py - this is a reference file with 
# sensitive data for the robo investing system.
# Peter Koppelman - July 12, 2020

import dash_html_components as html
import http.client
import json


# Email Password and account
password = 'NYUCapstone'
account = 'capstone.roboinvesting@gmail.com'

# Recipients of emails
# recipients = ['pbkoppelman@gmail.com', 'michael.shore93@gmail.com']
recipients = ['pbkoppelman@gmail.com']

# Database connectivity to fastrack
conn = http.client.HTTPSConnection("ftlightning.fasttrack.net")
x = 'GET'
y = "/v1/auth/login?account=300724&pass=1243OEIL&appid=F075C6E1-759C-4009-9B47-5FE284F31F55"
conn.request(x,y)
res = conn.getresponse()
data = json.loads(res.read())
appid = data['appid']
token = data['token']

# security list
sec_list = ["VOO", "PRULX", "VTIAX", "PFORX", "FDHY"]

# setting paths and naming database table paths.
# db_path = '/users/pkopp/python_diploma/Capstone/dev/apps'
# database = r"C:\users\pkopp\python_diploma\Capstone\dev\database\roboinvest.db"
db_path = '/roboinvest/apps'
database = r"C:\roboinvest\database\roboinvest.db"
