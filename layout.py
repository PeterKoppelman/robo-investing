
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol
import dash_table.FormatTemplate as FormatTemplate

import pandas as pd

HEADER_STYLE = {
    'display': 'flex', 
    'justifyContent': 'center',
    'display': 'block',
    'text-align': 'center',
    'background': 'rgb(0,191,255, .6)'
    }

OPEN_ACCOUNT_LABEL = {
    'display': 'inline-block',
    'width': '140px',
    'text-align': 'right'
}

OPEN_ACCOUNT_FORM = {
    'width': '1200px',
    'border-radius': '3px',
    'box-shadow': '0 0 200px rgba(255, 255, 255, 0.5), 0 1px 2px rgba(0, 0, 0, 0.3)',
    'font': '17px/20px "Lucida Grande", Tahoma, Verdana, sans-serif',
}

PORTFOLIO_LAYOUT = {
    'display': 'flex', 
    'justifyContent': 'center'
}

SLIDER_LAYOUT = {
    'font-size': '20px',
    'text-align': 'center',
    'margin-top': 0,
    'margin-right': '15%',
    'margin-bottom': 0,
    'margin-left': '15%'
}

def welcome():
    return html.Div([
        html.Div([
        html.H2('The Shore-Koppelman Group'),
        html.H3('Robo-Investing Tool'),
        ], style = HEADER_STYLE
    ),
    html.Br(),
    html.Br(),
    html.H5('Welcome to Robo-Investing! The app for personal investors. Feel free to create a sample portfolio.',
            style = {'text-align': 'center'}),
])


def journal_data_entry(app):
    return html.Div([
        html.Div([
        html.H2('The Shore-Koppelman Group'),
        html.H3('Robo-Investing Tool'),
            ], style = HEADER_STYLE
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H5('Enter deposit information from the Customer',
               style = {'text-align': 'center'}),
        html.Br(),
        html.Form([
            html.Br(),
            html.H5('Account Information',
                   style = {'font-weight ': 'bold'}
                   ),
                html.Label('Master Account:',
                    style = OPEN_ACCOUNT_LABEL
                    ),
                dcc.Input(id = 'master_account_number', 
                            type = 'text', 
                            minLength = 8, 
                            maxLength = 25,
                            debounce = True,
                            ),
                html.Label('Date:',
                    style = OPEN_ACCOUNT_LABEL
                    ),
                 dcc.Input(id = 'date_of_entry', 
                            type = 'text', 
                            minLength = 8, 
                            maxLength = 25,
                            debounce = True,
                            ),
                html.Label('Account Number:',
                    style = OPEN_ACCOUNT_LABEL
                    ),
                 dcc.Input(id = 'acct_number', 
                            type = 'text', 
                            minLength = 0, 
                            maxLength = 10,
                            debounce = True,
                            ),
                html.Br(),
                html.Br(),
                html.Br(),
                html.H5('Credit/Debit Information',
                   style = {'font-weight ': 'bold'}
                   ),
                html.Label('Debit (withdrawal):',
                    style = OPEN_ACCOUNT_LABEL
                    ),
                 dcc.Input(id = 'debit_amt', 
                            type = 'text', 
                            minLength = 5, 
                            maxLength = 25,
                            debounce = True,
                            ),
                html.Label('Credit (deposit):',
                    style = OPEN_ACCOUNT_LABEL
                    ),
                 dcc.Input(id = 'credit_amt', 
                            type = 'text', 
                            minLength = 5, 
                            maxLength = 25,
                            debounce = True,
                            ),
                html.Label('Description:',
                    style = OPEN_ACCOUNT_LABEL
                    ),
                 dcc.Input(id = 'description', 
                            type = 'text', 
                            minLength = 5, 
                            maxLength = 50,
                            debounce = True,
                            ),
                html.Br(),
                html.Br(),
                html.Br(),
                html.H5('Employee Information',
                     style = {'font-weight ': 'bold'}
                     ),
                html.Label('Last Name: ',
                    style = OPEN_ACCOUNT_LABEL 
                    ), 
                dcc.Input(type = 'text',
                        id = 'ee_lname', 
                        minLength = 8, 
                        maxLength = 40,
                        debounce = True,
                    ),
                html.Label('Employee Number: ', 
                    style = OPEN_ACCOUNT_LABEL
                    ),
                    dcc.Input(type = 'password',
                        id = 'ee_tin', 
                        minLength = 8, 
                        maxLength = 25,
                        debounce = True,
                    ),
                html.Label('Date of Birth: ', 
                    style = OPEN_ACCOUNT_LABEL
                    ),
                dcc.Input(type = 'password',
                        id = 'ee_dob', 
                        minLength = 8, 
                        maxLength = 25,
                        debounce = True,
                    ),
                html.Br(),
                html.Br(),
                html.Div([
                dbc.Button('Submit',
                    id = 'journal_submit_button',
                    color = 'primary',
                    n_clicks = 0,
                    className='mr-1'
                ),
                ], style = {'text-align': 'left'},
            ),
            # html.Div(id = 'journal_entry_complete')
        ],
    ), html.Div(id = 'journal_entry_complete')
])


def client_login(app):
    return html.Div([
        html.Div([
        html.H2('The Shore-Koppelman Group'),
        html.H3('Robo-Investing Tool'),
        ], style = HEADER_STYLE
    ),
    html.Br(),
    html.Br(),
    html.H5('Client Login',
        style = {'text-align': 'center'}),
    html.Br(),
    html.Form([
    html.Label('Last Name: ', 
        ), 
        dcc.Input(type = 'text',
                    id = 'client_lname', 
                    placeholder = 'Last Name',
                    minLength = 8, 
                    maxLength = 40,
                    debounce = True,
        ),

    html.Br(),
    html.Br(),
    html.Label('TIN: ', 
        ),
        dcc.Input(type = 'password',
                    id = 'client_tin', 
                    placeholder = 'Your Tax ID Number',
                    minLength = 8, 
                    maxLength = 25,
                    debounce = True,
        ),
    html.Br(),
    html.Br(),
    html.Label('Date of Birth: ', 
        ),
        dcc.Input(type = 'password',
                    id = 'client_dob', 
                    placeholder = 'Date of Birth',
                    minLength = 8, 
                    maxLength = 25,
                    debounce = True,
        ),

    html.Br(),
    html.Br(),
    dbc.Button('Login',
        id = 'login_button',
        color = 'primary',
        n_clicks = 0,
        className='mr-1'
    ), 
    ], style = { 
        'justifyContent': 'center',
        'text-align': 'center'
        }
    ),html.Div(id = 'client_login_to_account', style = {'display': 'none'}),
    # html.Div(id = 'client_data', style = {'display': 'none'})
])


def open_account(app):
    return html.Div([
        html.Div([
        html.H2('The Shore-Koppelman Group'),
        html.H3('Robo-Investing Tool'),
        ],
        style = HEADER_STYLE 
    ),
    html.Br(),
    html.Br(),
    html.H5('To open an account please fill out the following information',
        style = {'text-align': 'center'}),
    html.Br(),
    html.Br(),
    html.Form([
        # html.Fieldset([
        html.Label('Name',
           style = {'font-weight ': 'bold'}),
        html.Br(),
        html.Label('First Name:',
            style = OPEN_ACCOUNT_LABEL),
         dcc.Input(id = 'fname', 
                    type = 'text', 
                    minLength = 2, 
                    maxLength = 25,
                    debounce = True,
                    ),
        html.Label('Middle Initial:',
            style = OPEN_ACCOUNT_LABEL),
         dcc.Input(id = 'm_init', 
                    type = 'text', 
                    minLength = 0, 
                    maxLength = 2,
                    debounce = True,
                    ),
        html.Label('Last Name:',
            style = OPEN_ACCOUNT_LABEL),
         dcc.Input(id = 'lname', 
                    type = 'text', 
                    minLength = 2, 
                    maxLength = 25,
                    debounce = True,
                    ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Label('Address',
            style = {'font-weight': 'bold'}),
        html.Br(),
        html.Label('Street Address:',
            style = OPEN_ACCOUNT_LABEL),
         dcc.Input(id = 'addr', 
                    type = 'text', 
                    minLength = 2, 
                    maxLength = 25,
                    debounce = True,
                    ),
        html.Label('City:',
            style = OPEN_ACCOUNT_LABEL),
         dcc.Input(id = 'city', 
                    type = 'text', 
                    minLength = 2, 
                    maxLength = 25,
                    debounce = True,
                    ),
        html.Br(),
        html.Label('State:',
            style = OPEN_ACCOUNT_LABEL),
         dcc.Input(id = 'st', 
                    type = 'text', 
                    minLength = 2, 
                    maxLength = 25,
                    debounce = True,
                    ),
        html.Label('Zip Code:',
            style = OPEN_ACCOUNT_LABEL),
         dcc.Input(id = 'zipcode', 
                    type = 'text', 
                    minLength = 5, 
                    maxLength = 10,
                    debounce = True,
                    ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Label('Other Information',
            style = {'font-weight': 'bold'}),
        html.Br(),
        html.Label('Email Address:',
            style = OPEN_ACCOUNT_LABEL),
         dcc.Input(id = 'email', 
                    type = 'text', 
                    minLength = 8, 
                    maxLength = 25,
                    debounce = True,
                    ),
        html.Label('Social Security or TIN number:',
            style = OPEN_ACCOUNT_LABEL),
         dcc.Input(id = 'tin', 
                    type = 'text', 
                    minLength = 8, 
                    maxLength = 25,
                    debounce = True,
                    ),
        html.Label('Date of Birth:',
            style = OPEN_ACCOUNT_LABEL),
         dcc.Input(id = 'dob', 
                    type = 'text', 
                    minLength = 8, 
                    maxLength = 25,
                    debounce = True,
                    ),

        html.Br(),
        html.Br(),
        html.Br(),
        html.Label('Password has min length 8, max length 25.',
            style = {'font-weight': 'bold'}),
        html.Br(),
        html.Label('Password:',
            style = OPEN_ACCOUNT_LABEL),
        dcc.Input(id = 'password', 
                   type = 'password', 
                   minLength = 8, 
                   maxLength = 25,
                   debounce = True,
                ),
        html.Br(),
        html.Br(),
        html.Label('Please note that our ABA routing number is 123456789 and our account number is 555-555-5555'),
        html.Label('Call us at 1.866.555.7575 and speak to one of our operators if you have questions concerning wiring us money'),
        html.Br(),
        html.Div([
            dbc.Button('Submit',
                id = 'account_opening_button',
                color = 'primary',
                n_clicks = 0,
                className='mr-1'
            ), 
        ], style = {'text-align': 'right'},
        ),   
        html.Div(id = 'open_account_button')
        # ]), ### end fieldset
        ], style = OPEN_ACCOUNT_FORM
    ),
], 
)


def sample_portfolio_layout(app, df_portfolio):
    return html.Div([
        html.Div([
        html.H2('The Shore-Koppelman Group'),
        html.H3('Robo-Investing Tool'),
        ], style = HEADER_STYLE 
    ),
    html.Br(),
    html.Br(),
    html.H5("Create a Sample Portfolio - it's free",
        style = {'text-align': 'center'}),
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
        ], style = PORTFOLIO_LAYOUT
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
        ], style = PORTFOLIO_LAYOUT
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
    ], style = SLIDER_LAYOUT
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
        # data = df_portfolio.to_dict('rows'),
        columns = [
            {'name': 'Security', 
                'id' : 'security'},
            {'name': 'Category',
                'id': 'category'},
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
        style_cell = {
            'textAlign' : 'center'
        },
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

def contact_layout(app):
    return html.Div([ 
        html.Div([
        html.H2('The Shore-Koppelman Group'),
        html.H3('Robo-Investing Tool'),
        ], style = HEADER_STYLE 
    ),
    html.Br(),
    html.Br(),
    html.H5('To send us a comment please fill out the information below:',
        style = {'text-align': 'center'}),

    html.Br(),
    dbc.Label('Name:'),
    dbc.Input(
        type = 'value',
        id = 'name',
        minLength = 3,
        maxLength = 100,
        valid = True,
        style = {'width': 400},
    ),
   
    dbc.Label('Email address:'),
    dbc.Input(
        type = 'email', 
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
    dbc.Label('Minimum 10 characters, maximum 500 characters'),
    dbc.Textarea(
        id = 'comment',
        maxLength = 500,
        required = True,
        rows = 6,
        spellCheck = True,
        valid = True
    ),

    html.Br(),
    dbc.Button('Submit',
        id = 'submit-email',
        color = 'primary',
        n_clicks = 0,
        className='mr-2'
    ), html.Div(id = 'email_to'),
])


def faq():
    return html.Div([
        html.Div([
        html.H2('The Shore-Koppelman Group'),
        html.H3('Robo-Investing Tool'),
        ], style = HEADER_STYLE 
    ),
    html.Br(),
    html.Br(),
    html.H4('FAQ Page',
        style = {'text-align': 'center'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.H5('Q: Who is the Shore-Koppelman Group?'),
        html.Div([
            html.H6('The Shore-Koppelman Group is made up of Michael Shore and Peter Koppelman.'),
            html.H6('The company came about as the capstone project for the python diploma program at NYU.'),
            html.H6("The principles decided that it wasn't that hard to do as good if not better a job than many money managers.")
            ], style = {'text-indent': '5em'}
        ),
        html.Br(),
        html.H5('Q: What is your investment strategy?'),
        html.Div([
            html.H6("The investment strategy is pretty simple. We take a look at the 3, 5 and 10 year return for securities in different"),
            html.H6('sectors to see who has the best returns. We then factor changes in general management at the at the firms and'),
            html.H6("changes in the management of the specific mutual funds. With EFTs we break things down sector"),
            html.H6('by sector and use those to compliment the mutual funds that we are investing in.')
            ], style = {'text-indent': '5em'}
        ),


        html.Br(),
        html.H5('Q: How often do you rebalance the portfolio?'),
        html.Div([
            html.H6("The principle's of the firm meet quarterly to determine if the securities in the portfolio should"),
            html.H6('be changed. They do a thorough analysis of market conditions, look at returns and speak to the money'),
            html.H6('managers running the mutual funds and ETFs that the firm is invested in.')
            ], style = {'text-indent': '5em'}
        ),
        html.Br(),
        html.H5('Q: How do you earn your fees?'),
        html.Div([
            html.H6('We take 2% of the fees undermanagement plus a percentage of the profit. The percentage is a sliding scale.'),
            html.H6('The more money that you have under management, the smaller the percentage that we take from your profits.')
            ], style = {'text-indent': '5em'}
        ),
    ]),

])

