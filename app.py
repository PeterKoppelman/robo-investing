
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Div([
    	html.H1(children='Welcome to Robo-Investing!'),
    	html.H4(children='The app for personal investors!'),
    	html.Br(),
    	html.H6(children = 'This application will create a portfolio for you based on your age and risk tolerance')
    ], style = {'text-align': 'center'}
    ),

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
    html.Div(children = ['What is your risk tolerance (1 is the lowest, 10 is the highest and 5 is neutral)?',
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
    ]),

    html.Div(children = ['Would you like to open an account with us using this portfolio?',
		dcc.RadioItems(
			options = [
				{'label': 'Yes', 'value': 'Yes'},
				{'label': 'No', 'value': 'No'},
			],
			value = ''
		), 
	], style = {'position': 'absolute',
	     		'bottom': '15%',
	      		'right': '5%',
	      		'text-align': 'center'}
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


if __name__ == '__main__':
    app.run_server(debug=True)
