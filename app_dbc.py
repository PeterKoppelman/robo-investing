# App2.py - front end using dash bootstrap components
# July 2, 2020 Peter Koppelman

import dash as dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
# from dash import no_update

import contact_us_dbc as contact_us
import welcome_dbc as welcome
import calc_portfolio_dbc as calc_portfolio


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import reference

import http.client
import json

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H4("Robo Investing Tool", className="display-5"),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("Welcome", href="/page-1", id="page-1-link"),
                dbc.NavLink("Login", href="/page-2", id="page-2-link"),
                dbc.NavLink("Open an account", href="/page-3", id="page-3-link"),
                dbc.NavLink("Create a portfolio", href="/page-4", id="page-4-link"),
                dbc.NavLink("Contact Us", href="/page-5", id="page-5-link"),
                dbc.NavLink("FAQ", href="/page-6", id="page-6-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

page_layout = html.Div([
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

@app.callback(
    [Output('counter', 'children')],
    [Input('submit-email', 'n_clicks')],
    [State('name', 'value'),
    State('email-addr', 'value'),
    State('comment', 'value')]
)

def send_email(n, name, email_addr, comment):
    if n > 0:
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Email message to the Shore-Koppelman Group'
        message_body = 'An email came from: '+ name+'\n' 'At email address: '+ email_addr+'\n' 'Comment: '+ comment
        message.attach(MIMEText(message_body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(reference.account, reference.password)

            # Sent from, sent to, message
            server.sendmail(reference.account, reference.recipients, message.as_string())
            server.quit()
            return [f'\nThank you your email has been sent']
        except Exception as e:
            print('email did not send ', e)
            return[f'Sorry, there was a problem sending your email']
    else:
        return ['']

get_data = html.Div([ #html.Div(children=[
    html.Div(
        [
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
                    ),
            html.H5(id = 'id-age')
        ], style = {'display': 'flex', 
                'justifyContent': 'center'}
    ),

    html.Br(),
    html.H5(children = ['Enter the amount of money would you like to invest): ',
        dcc.Input(style = {'width': 125}, 
                    id = 'my-amount', 
                    value = 5000,
                    type = 'number', 
                    min = 5000, 
                    max = 100000,
                    ),
            html.H5(id = 'id-amount')
        ], style = {'display': 'flex', 
                'justifyContent': 'center'}
    ),

    html.Br(),
    html.H5(children = ['What is your risk tolerance (1 is the lowest, 10 is the highest and 5 is neutral)',
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
    html.Br(),
    html.H5(children = ['Your recommended portfolio is as follows:',
        html.H5(children = [
            html.Tr([html.Td(['Domestic Equity:']), html.Td(id = 'domestic_equity')]),
            html.Tr([html.Td(['International Equity:']), html.Td(id = 'intl_equity')]),
            html.Tr([html.Td(['Government Bonds:']), html.Td(id = 'govy_bonds')]),
            html.Tr([html.Td(['Corporate Bonds:']), html.Td(id = 'corp_bonds')]),
            html.Tr([html.Td(['International Bonds:']), html.Td(id = 'intl_bonds')]),
        ], style = {'text-indent': '50px'}
    ),
    ], style = {'font-size': '20px'}
    )
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
    # 1) domestic equity
    # 2) international equity
    # 3) domestic government bonds
    # 4) domestic corporate bonds
    # 5) international bonds.
    # Each list is for a group 20, 25,30, 35, 40, etc up to 65
    # account_bal = amount
   #  # portfolio = [0.25, 0.1, 0.3, 0.1, 0.25]
    conn = http.client.HTTPSConnection("ftlightning.fasttrack.net")
    headers = {
        'appid': "F075C6E1-759C-4009-9B47-5FE284F31F55",
        'token': "CD3266E5-7E3A-4150-A676-CF32B0F80167"
    }
    sec_list = ["VOO", "PRULX", "VTIAX", "PFORX", "FDHY", "SPY"]
    sec_val_list = []

    for sec in sec_list:
        conn.request("GET", "/v1/data/" + sec + "/divadjprices", headers=headers)
        res = conn.getresponse()
        data = res.read()
        dic = json.loads(data)
        sec_val_list.append(dic["prices"][-1])

    # The base portfolio is used when the risk tolerance is 5 (neutral) 
    # For positions 0 - 4 see above.
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
        portfolio[4] += portfolio[4] * (adj * (5 - risk_tolerance))
    elif risk_tolerance > 5:
        portfolio[0] += portfolio[0] * (adj * (risk_tolerance - 5))
        portfolio[1] += portfolio[1] * (adj * (risk_tolerance - 5))
        portfolio[2] += portfolio[2] * (-adj * (risk_tolerance - 5))
        portfolio[3] += portfolio[3] * (-adj * (risk_tolerance - 5))
        portfolio[4] += portfolio[4] * (-adj * (risk_tolerance - 5))


    dom_stock  = int((amount * portfolio[0]) / sec_val_list[0])
    dom_stock_rem = portfolio[0] * amount - (dom_stock * sec_val_list[0])
    gov_bond  = int((amount * portfolio[1]) / sec_val_list[1])
    gov_bond_rem = portfolio[1] * amount - (gov_bond * sec_val_list[1])
    int_stock  = int((amountl * portfolio[2]) / sec_val_list[2])
    int_stock_rem = portfolio[2] * amount - (int_stock * sec_val_list[2])
    int_bond  = int((amount * portfolio[3]) / sec_val_list[3])
    int_bond_rem = portfolio[3] * amount - (int_bond * sec_val_list[3])
    corp_bond  = int(amount * portfolio[4] / sec_val_list[4])
    corp_bond_rem = portfolio[4] * amount - (corp_bond * sec_val_list[4])
    ttl_rem = dom_stock_rem + gov_bond_rem + int_stock_rem + int_bond_rem + corp_bond_rem
    rem_spy = ttl_rem / sec_val_list[5]

    # dom_stock  = int((account_bal * portfolio[0]) / sec_val_list[0])
    # dom_stock_rem = portfolio[0] * account_bal - (dom_stock * sec_val_list[0])
    # gov_bond  = int((account_bal * portfolio[1]) / sec_val_list[1])
    # gov_bond_rem = portfolio[1] * account_bal - (gov_bond * sec_val_list[1])
    # int_stock  = int((account_bal * portfolio[2]) / sec_val_list[2])
    # int_stock_rem = portfolio[2] * account_bal - (int_stock * sec_val_list[2])
    # int_bond  = int((account_bal * portfolio[3]) / sec_val_list[3])
    # int_bond_rem = portfolio[3] * account_bal - (int_bond * sec_val_list[3])
    # corp_bond  = int(account_bal * portfolio[4] / sec_val_list[4])
    # corp_bond_rem = portfolio[4] * account_bal - (corp_bond * sec_val_list[4])
    # ttl_rem = dom_stock_rem + gov_bond_rem + int_stock_rem + int_bond_rem + corp_bond_rem
    # rem_spy = ttl_rem / sec_val_list[5]



    return ('${:,.2f}'.format(portfolio[0]/100 * amount), 
        '${:,.2f}'.format(portfolio[1]/100 * amount), 
        '${:,.2f}'.format(portfolio[2]/100 * amount), 
        '${:,.2f}'.format(portfolio[3]/100 * amount), 
        '${:,.2f}'.format(portfolio[4]/100 * amount))


content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 7)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 7)]


@app.callback(Output("page-content", "children"), 
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == '/page-1':
        return welcome.welcome
    elif pathname == "/page-2":
        return html.P('Log In Page')
    elif pathname == "/page-3":
        return html.P('Open an account')
    elif pathname == "/page-4":
        app.layout = html.Div([dcc.Location(id="url"), get_data])
        return get_data
    elif pathname == "/page-5":
        app.layout = html.Div([dcc.Location(id="url"), page_layout])
        return page_layout
    elif pathname == '/page-6':
        return html.P('Welcome to the FAQ Page')


if __name__ == "__main__":
    app.run_server(debug=True)

