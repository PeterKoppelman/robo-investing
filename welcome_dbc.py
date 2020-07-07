# welcome.py - this is the welcome page to the robo project
# Peter Koppelman July 3, 2020


import dash_bootstrap_components as dbc
import dash_html_components as html

welcome = dbc.Toast(
    [html.H3('Welcome to Robo-Investing!', className = 'x1'),
    html.H3('The app for personal investors', className = 'x1'),
    html.H3('Bought to you by The Shore-Koppelman Group', className = 'x1'),
    html.Br(),
    html.H3('Welcome to our Website, please feel free to create a portfolio')],
    # header="Welcome to Robo-Investing!", className = 'x1',9295
    style = {'text-align': 'center',
    		'font': 'bold 1.5em Times, "Times New Roman", serif',
    		'display': 'flex',
    		'align-items': 'center',
    		'justify-content': 'center',
    		'margin': '30px',
    		'max-width': '600px',
    		'margin-left': '25%'
    	}
	) 
