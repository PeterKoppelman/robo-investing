'''This is the layout program for the roboinvest program.
Peter Koppelman September 9, 2020'''
from datetime import date

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_table.FormatTemplate as FormatTemplate

# The following are Dash's version of CSS
# Everything gets put in a dictionary and called when needed.
LABEL = {
    'display': 'inline-block',
    'width': '180px',
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

TEXT_ALIGN_CENTER = {
     'text-align': 'center'
}

CLIENT_PADDING = {
    'padding': '5px 1em 0 2em'
}

LOGIN_STYLE = {
    'width': '340px',
    'margin': '50px auto',
    'font-size': '15px',
    'margin-bottom': '15px',
    'background': '#f7f7f7',
    'box-shadow': '0px 2px 2px rgba(0, 0, 0, 0.3)',
    'padding': '30px'
}


def welcome():
    '''This is the welcome screen.'''
    return html.Div([
    html.Br(),
    html.Br(),
    html.H5('Welcome to Robo-Investing! The app for personal investors. \
        Feel free to create a sample portfolio.',
            style = TEXT_ALIGN_CENTER ),
])

def login():
    '''This is the login screen.'''
    return html.Div([
        html.Div(children = [
            html.Div(children = [
                html.Label('Email Address',
                    ),
                dcc.Input(type = 'email',
                    id = 'email',
                    placeholder = 'email@example.com',
                    minLength = 7,
                    maxLength = 40,
                    debounce = True,
                    className = 'form-control',
                ),
                ], className = 'form-group'
            ),
            html.Div(children = [
                html.Label('Password:',
                    ),
                dcc.Input(type = 'password',
                    id = 'password',
                    placeholder = 'Password',
                    minLength = 8,
                    maxLength = 25,
                    debounce = True,
                    className = 'form-control'
                ),
            ], className = 'form-group'
            ),
            dbc.Button('Submit',
                id = 'login_submit',
                color = 'primary',
                className = 'mr-1',
                n_clicks = 0),
        ],
        style = LOGIN_STYLE,
        ),
    html.Div(id = 'record', style = {'display': 'none'}),
    ],
)


# def present_customer_data_layout(app, record):
def present_customer_data_layout():
    '''This is the screen layout for the customer data. This has not been implemented yet.'''
    return html.Div([
    html.Br(),
    html.Br(),
    html.H5('Client Information',
        style = TEXT_ALIGN_CENTER ),
    html.Br(),
    dash_table.DataTable(
        id='record',
        columns = [
            {'name': 'Customer Name',
                'id' : 'name'},
            {'name': 'Account Number',
                'id': 'account number'},
            {'name': 'Account Balance',
                'id' : 'account balance',
                'type' : 'numeric',
                'format': FormatTemplate.money(2)},
            {'name': 'Date of Transaction',
                'id' : 'date of entry'},
            {'name': 'Transaction Type',
                'id' : 'transaction type'},
            {'name': 'Transaction Amount',
                'id' : 'transaction amount',
                'type' : 'numeric',
                'format': FormatTemplate.money(2)},
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
    html.Div(id = 'customer_record')
])


def sample_portfolio_layout(app, df_portfolio):
# def sample_portfolio_layout():
    '''This is the layout of the sample portfolio.'''
    return html.Div([
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
    html.Div(children = ['What is your risk tolerance (1 is the lowest, \
        10 is the highest and 5 is neutral)',
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
    html.H5(children = ['The dollar allocation to each sector will change every day \
        that the financial markets are open at approximately 6:45 pm.'],
            style = TEXT_ALIGN_CENTER ),
    html.H5(children = ['This is the time that we get new market data'],
            style = TEXT_ALIGN_CENTER ),
    html.Br(),
    dash_table.DataTable(
        id='df_portfolio',
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



def open_account():
    '''This is the screen layout to open an account.'''
    return html.Div([
    html.Br(),
    html.Form([
        html.Br(),
        html.Label('Name',
           style = {'font-weight ': 'bold'}),
        html.Br(),
        html.Label('First Name:',
            style = LABEL),
        dcc.Input(id = 'fname',
                    type = 'text',
                    minLength = 2,
                    maxLength = 25,
                    debounce = True,
                    ),
        html.Label('Middle Initial:',
            style = LABEL),
        dcc.Input(id = 'm_init',
                    type = 'text',
                    minLength = 0,
                    maxLength = 2,
                    debounce = True,
                    ),
        html.Label('Last Name:',
            style = LABEL),
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
            style = LABEL),
         dcc.Input(id = 'addr',
                    type = 'text',
                    minLength = 2,
                    maxLength = 25,
                    debounce = True,
                    ),
        html.Label('City:',
            style = LABEL),
         dcc.Input(id = 'city',
                    type = 'text',
                    minLength = 2,
                    maxLength = 25,
                    debounce = True,
                    ),
        html.Br(),
        html.Label('State:',
            style = LABEL),
         dcc.Input(id = 'st',
                    type = 'text',
                    minLength = 2,
                    maxLength = 25,
                    debounce = True,
                    ),
        html.Label('Zip Code:',
            style = LABEL),
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
            style = LABEL),
         dcc.Input(id = 'email',
                    type = 'text',
                    minLength = 8,
                    maxLength = 25,
                    debounce = True,
                    ),
        html.Label('Social Security or TIN number:',
            style = LABEL),
         dcc.Input(id = 'tin',
                    type = 'text',
                    minLength = 8,
                    maxLength = 25,
                    debounce = True,
                    ),
        html.Label('Date of Birth:',
            style = LABEL),
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
            style = LABEL),
        dcc.Input(id = 'password',
                   type = 'password',
                   minLength = 8,
                   maxLength = 25,
                   debounce = True,
                ),
        html.Br(),
        html.Br(),
        html.Label('Please note that our ABA routing number is 123456789 and our \
            account number is 555-555-5555'),
        html.Label('Call us at 1.866.555.7575 and speak to one of our operators \
            if you have questions concerning wiring us money'),
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
        ], style = OPEN_ACCOUNT_FORM
    ),
],
)


def contact_layout():
    '''This is the screen layout to send us an email.'''
    return html.Div([
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
    '''This is our faq screen.'''
    return html.Div([
    html.Br(),
    html.Br(),
    html.Div([
        html.H5('Q: Who is the Shore-Koppelman Group?'),
        html.Div([
            html.H6('The Shore-Koppelman Group is made up of Michael Shore and Peter Koppelman.'),
            html.H6('The company came about as the capstone project for the python \
                diploma program at NYU.'),
            html.H6("The principles decided that it wasn't that hard to do as good \
                if not better a job than many money managers.")
            ], style = {'text-indent': '5em'}
        ),
        html.Br(),
        html.H5('Q: What is your investment strategy?'),
        html.Div([
            html.H6("The investment strategy is pretty simple. We take a look at the 3, 5 \
                and 10 year return for securities in different"),
            html.H6('sectors to see who has the best returns. We then factor changes in \
                general management at the at the firms and'),
            html.H6("changes in the management of the specific mutual funds. With EFTs we \
                break things down sector"),
            html.H6('by sector and use those to compliment the mutual funds that we are \
                investing in.')
            ], style = {'text-indent': '5em'}
        ),


        html.Br(),
        html.H5('Q: How often do you rebalance the portfolio?'),
        html.Div([
            html.H6("The principle's of the firm meet quarterly to determine if the \
                securities in the portfolio should"),
            html.H6('be changed. They do a thorough analysis of market conditions, \
                look at returns and speak to the money'),
            html.H6('managers running the mutual funds and ETFs that the firm is \
                invested in.')
            ], style = {'text-indent': '5em'}
        ),
        html.Br(),
        html.H5('Q: How do you earn your fees?'),
        html.Div([
            html.H6('We take 2% of the fees undermanagement plus a percentage of the profit. \
                The percentage is a sliding scale.'),
            html.H6('The more money that you have under management, the smaller the \
                percentage that we take from your profits.')
            ], style = {'text-indent': '5em'}
        ),
    ]),

])

# def journal_data_entry(app, cust_info, ee_info, acct_info):
def journal_data_entry(cust_info, ee_info, acct_info):
    '''This is the screen layout to enter customer deposits and withdrawals.'''
    return html.Div([
        html.Br(),
        html.Br(),
        html.Form([
            html.Br(),
            html.H5('General Information',
                   style = {'font-weight ': 'bold'}
                   ),
                html.Label('Date:',
                    style = LABEL
                    ),
                    dcc.DatePickerSingle(
                        id = 'date_of_entry',
                        date = date.today().strftime('%m/%d/%Y'),
                        style = {'display': 'inline-block',
                                'position': 'relative',
                                'left': 2,
                                'top': 4,
                                }
                        ),
                html.Label('Customer:',
                    style = LABEL
                    ),
                dcc.Dropdown(
                    id = 'customer',
                    options = cust_info,
                        style = {'fontsize': 24,
                                'width': 225,
                                'display': 'inline-block',
                                'position': 'relative',
                                'left': 2,
                                'top': 5}
                            ),
                html.Label('Account Number:',
                    style = LABEL
                    ),
                dcc.Dropdown(
                    id = 'acct_number',
                    options = acct_info,
                    style = {'fontsize': 24,
                            'width': 225,
                            'display': 'inline-block',
                            'position': 'relative',
                            'left': 2,
                            'top': 5}
                        ),
                html.Br(),
                html.Br(),
                html.Br(),
                html.H5('Transaction Information',
                   style = {'font-weight ': 'bold'}
                   ),
                html.Label('Transaction type:',
                    style = LABEL
                    ),
                dcc.Dropdown(
                    id = 'transaction_type',
                    options = [
                        {'label': 'Initial Deposit', 'value': 'Initial Deposit'},
                        {'label': 'Deposit', 'value': 'Deposit'},
                        {'label': 'Withdrawal', 'value': 'Withdrawal'}],
                        style = {'fontsize': 24,
                                'width': 175,
                                'display': 'inline-block',
                                'position': 'relative',
                                'left': 2,
                                'top': 5}
                            ),
                html.Label('Transaction Amount: ',
                    style = LABEL
                    ),
                dcc.Input(id = 'transaction_amount',
                            type = 'number',
                            minLength = 1,
                            maxLength = 10,
                            debounce = True,
                            ),
                html.Br(),
                html.Br(),
                html.Br(),
                html.H5('Employee Information',
                     style = {'font-weight ': 'bold'}
                     ),
                html.Label('Last Name: ',
                        style = LABEL
                    ),
                    dcc.Dropdown(
                    id = 'ee_lname',
                    options = ee_info,
                        style = {'fontsize': 24,
                                'width': 200,
                                'display': 'inline-block',
                                'position': 'relative',
                                'left': 2,
                                'top': 5}
                            ),
                html.Label('Employee Number: ',
                    style = LABEL
                    ),
                    dcc.Input(type = 'password',
                        id = 'ee_tin',
                        minLength = 8,
                        maxLength = 25,
                        debounce = True,
                    ),
                html.Label('Date of Birth: ',
                    style = LABEL
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
