# reference.py - this is a reference file with 
# sensitive data for the robo investing system.
# Peter Koppelman - July 12, 2020

# Email Password anc account
password = 'NYUCapstone'
account = 'capstone.roboinvesting@gmail.com'

# Recipients of emails
# recipients = ['pbkoppelman@gmail.com', 'michael.shore93@gmail.com']
recipients = ['pbkoppelman@gmail.com']

# Fastrack Investors appid and token
# header = 'appid': "F075C6E1-759C-4009-9B47-5FE284F31F55",
#    		 'token': "CD3266E5-7E3A-4150-A676-CF32B0F80167"

# base portfolio
base_portfolio = [[55,30,5,5,5], [50,30,10,5,5], [45,30,10,10,5], [45,25,10,10,10], [40,25,15,10,10],
	[40,20,15,15,10], [35,15,20,20,10], [30,15,25,20,10], [25,15,25,20,10], [25,15,30,25,5]]


 # for each increase or decrease in the risk tolerance the portfolio will move 2.5% in either a riskier
      # direction (more equities) or more conservative (more fixed income). The 2.5% increase in risk will be 
      # shared equally by the equity pieces of the portfolio. The 2.5% decrease in risk will be shared 
      # equally by the domestic bond peices of the portfolio. PK 6/29/2020
adj = .0125


# security list
# sec_list = ["VOO", "PRULX", "VTIAX", "PFORX", "FDHY", "SPY"]