
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol
import dash_table.FormatTemplate as FormatTemplate

import pandas as pd

def contact_layout(app):
    return html.Div([
        dbc.Label('To send us a comment please fill out the information below'),
        html.Br(),
        dbc.Label('Name:', html_for="name"),
        dbc.Input(
            type = 'value',
            id = 'name',
            minLength = 3,
            maxLength = 100,
            valid = True,
            style = {'width': 400}
        ),
       
        dbc.Label('Email address:', html_for="email_addr"),
        dbc.Input(
            type="value", 
            id='email-addr', 
            minLength = 7,
            maxLength = 30,
            valid = True,
            style = {'width': 400}
        ),

        html.Br(),
        html.Br(),
        dbc.Label('Please type your comment below:'),
        html.Br(),
        dbc.Label('Minimum 10 characters, maximum 1,000 characters', html_for="comment"),
        dbc.Textarea(
            id = 'comment',
            maxLength = 1000,
            required = True,
            rows = 10,
            spellCheck = True,
            valid = True
        ),

        html.Br(),
        dbc.Button('Submit',
            id = 'submit-email',
            color = 'primary',
            n_clicks = 0,
            className='mr-2'
        ), html.Div(id = 'counter'),
])


# def sample_portfolio_layout(app,x_portfolio):
def sample_portfolio_layout(app, df_portfolio):
    return html.Div([
        html.Div([
        html.H2('The Shore-Koppelman Group'),
        html.H3('Robo-Investing Tool'),
        html.H4("Create a Sample Portfolio - it's free"),
        ], style = {'display': 'flex', 
                    'justifyContent': 'center',
                    'display': 'block',
                    'text-align': 'center'}
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H5(children = ['Please enter your age (minimum 18 and maximum 99): ',
            dcc.Input(style = {'width': 80}, 
                        id = 'my-age', 
                        value = 25,
                        type = 'number', 
                        min = 18, 
                        max = 99,
                        debounce = True
                        ),

                html.H6(id = 'id-age')
            ], style = {'display': 'flex', 
                    'justifyContent': 'center'}
        ),

        html.Br(),
        html.H5(children = ['Enter the amount of money would you like to invest $): ',
            dcc.Input(style = {'width': 125}, 
                        id = 'my-amount', 
                        value = 5000,
                        type = 'number', 
                        min = 5000, 
                        max = 100000,
                        debounce=True
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
            ), html.Div(id = 'risk-tolerance-output-slider'),
        ], style = {'font-size': '20px',
                    'text-align': 'center',
                    'margin-top': 0,
                    'margin-right': '15%',
                    'margin-bottom': 0,
                    'margin-left': '15%'}
        ),

        html.Br(),
        html.Br(),
        html.H5(children = ['The dollar allocation to each sector will change every day that the financial markets are open at approximately 6:45 pm.'],
                style = {'textAlign' : 'center'}),
        html.H5(children = ['This is the time that we get new market data'],
                style = {'textAlign' : 'center'}),
        html.Br(),
        dash_table.DataTable(
            id='df_portfolio',
            data = df_portfolio.to_dict('rows'),
            columns = [
                {'name': 'Sector', 
                    'id' : 'sector'},
                {'name': 'Shares', 
                    'id' : 'shares'},
                {'name': 'Share Price', 
                    'id' : 'share price',
                    'type' : 'numeric',
                    'format': FormatTemplate.money(2)
                },
                {'name': 'Total Cost', 
                    'id' : 'total cost',
                    'type' : 'numeric',
                    'format': FormatTemplate.money(2)
                 },
                ],
            style_header = {
                'backgroundColor': 'rgb(230,230,230)', 
                'font-weight' : 'bold',
            },
            style_cell = {'textAlign' : 'center'},
            style_data_conditional=
            [
                {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
            ],  
            style_table = {
                'maxHeight': '300px', 
                'overflowY' : 'scroll',
                'font-family': 'sans-serif',
                'font-size': '24',
            } 
        ), 
        html.Div(id = 'portfolio_layout')
])


def welcome():
    return html.Div([
        html.Div([
        html.H2('The Shore-Koppelman Group'),
        html.H3('Robo-Investing Tool'),
        html.Br(),
        html.H3('Welcome to Robo-Investing!'),
        html.H3('The app for personal investors'),
        html.Br(),
        html.H3('Welcome to our website, feel free to create a sample portfolio')
    ],
        style = {'text-align': 'center',
                'font': 'bold 1.5em Times, "Times New Roman", serif'
        }
    )
])

def login():
    return html.Div([
        html.Div([
        html.H2('The Shore-Koppelman Group'),
        html.H3('Robo-Investing Tool'),
        html.Br(),
        html.Br(),
        html.H4('Login Id:'),
        html.H4('Password:')
        ], style = {'display': 'flex', 
                    'justifyContent': 'center',
                    'display': 'block',
                    'text-align': 'center'}
        ),
    
])


def open_account():
        return html.Div([
        html.Div([
        html.H2('The Shore-Koppelman Group'),
        html.H3('Robo-Investing Tool'),
        html.Br(),
        html.Br(),
        html.H4('Account Opening Page - under construction')
        ], style = {'display': 'flex', 
                    'justifyContent': 'center',
                    'display': 'block',
                    'text-align': 'center'}
        ),
    
])


def faq():
        return html.Div([
        html.Div([
        html.H2('The Shore-Koppelman Group'),
        html.H3('Robo-Investing Tool'),
        html.Br(),
        html.Br(),
        html.H4('FAQ Page - under construction')
        ], style = {'display': 'flex', 
                    'justifyContent': 'center',
                    'display': 'block',
                    'text-align': 'center'}
        ),
    
])

