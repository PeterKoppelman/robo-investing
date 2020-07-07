# calculate the portfolio
# July 5, 2020 - Michael Shore

import http.client
import json
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


get_data = html.Div(children=[
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
   	html.H6(children = ['Please enter your age (minimum 18 and maximum 99): ',
   		dcc.Input(style = {'width': 80}, 
   					id = 'my-age', 
   					value = 25,
   		 			type = 'number', 
   		 			min = 18, 
   		 			max = 99,
   					),
   			html.H6(id = 'id-age')
   		], style = {'display': 'flex', 
   				'justifyContent': 'center'}
    ),

    html.Br(),
   	html.H6(children = ['Enter the amount of money would you like to invest): ',
   		dcc.Input(style = {'width': 125}, 
   					id = 'my-amount', 
   					value = 5000,
   		 			type = 'number', 
   		 			min = 5000, 
   		 			max = 100000,
   					),
   			html.H6(id = 'id-amount')
   		], style = {'display': 'flex', 
   				'justifyContent': 'center'}
    ),

    html.Br(),
    html.Div(children = ['What is your risk tolerance (1 is the lowest, 10 is the highest and 5 is neutral)',
    	dcc.Slider(
    		id = 'risk-tolerance-slider',
    		min = 1,
			max = 10,
    		step = 1,
    		value = 5,
    		marks = {i: '{}'.format(i) for i in range(11)},
    	),
    	# html.Div(id = 'risk-tolerance-output-slider')
    ], style = {'font-size': '20px',
    			'text-align': 'center',
    			'margin-top': 0,
				'margin-right': '15%',
				'margin-bottom': 0,
				'margin-left': '15%'}
    ),

    html.Br(),
    html.Br(),
    html.Div(children = ['Your recommended portfolio is as follows:',
    	html.Tr([html.Td(['Domestic Equity:']), html.Td(id = 'domestic_equity')]),
    	html.Tr([html.Td(['International Equity:']), html.Td(id = 'intl_equity')]),
    	html.Tr([html.Td(['Government Bonds:']), html.Td(id = 'govy_bonds')]),
    	html.Tr([html.Td(['Corporate Bonds:']), html.Td(id = 'corp_bonds')]),
    	html.Tr([html.Td(['International Bonds:']), html.Td(id = 'intl_bonds')]),
    ], style = {'font-size': '20px'}
	),

    html.Div(children = ['Would you like to continue and open an account with us using this portfolio?',
		dcc.RadioItems(
			options = [
				{'label': 'Yes', 'value': 'Yes'},
				{'label': 'No', 'value': 'No'},
			],
			value = ''
		), 
	], style = {'position': 'relative',
	      		'right': '10%',
	      		'text-align': 'right'}
	),
])

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
 	# 1) domestic equity (SP500)
 	# 2) international equity
 	# 3) domestic government bonds
 	# 4) domestic corporate bonds
 	# 5) international bonds.
 	# Each list is for a group 20, 25,30, 35, 40, etc up to 65

	# The base portfolio is used when the risk tolerance is 5 (neutral)	
	base_portfolio = [[55,30,5,5,5], [50,30,10,5,5], [45,30,10,10,5], [45,25,10,10,10], [40,25,15,10,10],
		[40,20,15,15,10], [35,15,20,20,10], [30,15,25,20,10], [25,15,25,20,10], [25,15,30,25,5]]

	if (age >= 18 and age <= 22):
		portolio = base_portfolio[0]
	elif (age >= 23 and age <= 27):
		portfolio = base_portfolio[1]
	elif (age >= 28 and age <= 32):
		portfolio = base_portfolio[2]
	elif (age >= 33 and age <= 37):
		portfolio = base_portfolio[3]
	elif (age >= 38 and age <= 42):
		portfolio = base_portfolio[4]
	elif (age >= 43 and age <= 47):
		portfolio = base_portfolio[5]
	elif (age >= 48 and age <= 52):
		portfolio = base_portfolio[6]
	elif (age >= 53 and age <= 57):
		portfolio = base_portfolio[7]
	elif (age >= 58 and age <= 62):
		portfolio = base_portfolio[8]
	else:
		portfolio = base_portfolio[9]

	# for each increase or decrease in the risk tolerance the portfolio will move 2.5% in either a riskier
 	# direction (more equities) or more conservative (more fixed income). The 2.5% increase in risk will be 
	# shared equally by the equity pieces of the portfolio. The 2.5% decrease in risk will be shared 
	# equally by the domestic bond peices of the portfolio. PK 6/29/2020
	adj = .0125

	if risk_tolerance < 5:
		portfolio[0] += portfolio[0] * (-adj * (5 - risk_tolerance))
		portfolio[1] += portfolio[1] * (-adj * (5 - risk_tolerance))
		portfolio[2] += portfolio[2] * (adj * (5 - risk_tolerance))
		portfolio[3] += portfolio[3] * (adj * (5 - risk_tolerance))
	elif risk_tolerance > 5:
		portfolio[0] += portfolio[0] * (adj * (risk_tolerance - 5))
		portfolio[1] += portfolio[1] * (adj * (risk_tolerance - 5))
		portfolio[2] += portfolio[2] * (-adj * (risk_tolerance - 5))
		portfolio[3] += portfolio[3] * (-adj * (risk_tolerance - 5))


	return ('${:,.2f}'.format(portfolio[0]/100 * amount), 
		'${:,.2f}'.format(portfolio[1]/100 * amount), 
		'${:,.2f}'.format(portfolio[2]/100 * amount), 
		'${:,.2f}'.format(portfolio[3]/100 * amount), 
		'${:,.2f}'.format(portfolio[4]/100 * amount))


 #    html.Div([
 #    	dcc.Textarea(
 #    		id = 'textarea',
 #    		value = 'Would you like to continue and open\n an account with us using this portfolio?',
 #    		style = {'width': '100%', 'height': 300},
 #    	),
	# 	dcc.RadioItems(
	# 		options = [
	# 			{'label': 'Yes', 'value': 'Yes'},
	# 			{'label': 'No', 'value': 'No'},
	# 		],
	# 		value = ''
	# 	), 
	# ], style = {'position': 'relative',
 #      			'right': '10%',
 #      			'text-align': 'right'}
	# ),




# if __name__ == '__main__':
#     app.run_server(debug=True)


# class Financial_Data:
#     def ft_query():
#         account_bal = 5000
#         asset_allocation = [0.25, 0.1, 0.3, 0.1, 0.25]
#         conn = http.client.HTTPSConnection("ftlightning.fasttrack.net")
#         headers = {
#                 'appid': "F075C6E1-759C-4009-9B47-5FE284F31F55",
#                 'token': "CD3266E5-7E3A-4150-A676-CF32B0F80167"
#                 }
#         sec_list = ["VOO", "PRULX", "VTIAX", "PFORX", "FDHY", "SPY"]

#         sec_val_list = []
#         for sec in sec_list:

#             conn.request("GET", "/v1/data/" + sec + "/divadjprices", headers=headers)

#             res = conn.getresponse()
#             data = res.read()
#             dic = json.loads(data)
#             sec_val_list.append(dic["prices"][-1])

#         dom_stock  = int((account_bal * asset_allocation[0]) / sec_val_list[0])
#         dom_stock_rem = asset_allocation[0] * account_bal - (dom_stock * sec_val_list[0])
#         gov_bond  = int((account_bal * asset_allocation[1]) / sec_val_list[1])
#         gov_bond_rem = asset_allocation[1] * account_bal - (gov_bond * sec_val_list[1])
#         int_stock  = int((account_bal * asset_allocation[2]) / sec_val_list[2])
#         int_stock_rem = asset_allocation[2] * account_bal - (int_stock * sec_val_list[2])
#         int_bond  = int((account_bal * asset_allocation[3]) / sec_val_list[3])
#         int_bond_rem = asset_allocation[3] * account_bal - (int_bond * sec_val_list[3])
#         corp_bond  = int(account_bal * asset_allocation[4] / sec_val_list[4])
#         corp_bond_rem = asset_allocation[4] * account_bal - (corp_bond * sec_val_list[4])
#         ttl_rem = dom_stock_rem + gov_bond_rem + int_stock_rem + int_bond_rem + corp_bond_rem
#         rem_spy = ttl_rem / sec_val_list[5]

#         print("Your portfolio consists of the following...")
#         print("{} shares of {} at {}.".format(dom_stock, sec_list[0], sec_val_list[0]))
#         print("{} shares of {} at {}.".format(gov_bond, sec_list[1], sec_val_list[1]))
#         print("{} shares of {} at {}.".format(int_stock, sec_list[2], sec_val_list[2]))
#         print("{} shares of {} at {}.".format(int_bond, sec_list[3], sec_val_list[3]))
#         print("{} shares of {} at {}.".format(corp_bond, sec_list[4], sec_val_list[4]))
#         print("{} shares of {} at {}.".format(round(rem_spy, 4), sec_list[5], sec_val_list[5]))

#         return sec_val_list
#         return dom_stock
#         return dom_stock_rem
#         return gov_bond
#         return gov_bond_rem
#         return int_stock
#         return int_stock_rem
#         return int_bond
#         return int_bond_rem
#         return corp_bond
#         return corp_bond_rem
#         return ttl_rem
#         return rem_spy

# # if __name__ == "__main__":
# #     Financial_Data.ft_query()