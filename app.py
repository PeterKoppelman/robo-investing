# App2.py - front end using dash bootstrap components
# July 2, 2020 Peter Koppelman

import dash as dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from apps import layout, callbacks, reference

import pandas as pd

from sqlalchemy import Column, Date, String, create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


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

TEXT_ALIGN_CENTER = {
     'text-align': 'center'
}

HEADER_STYLE = {
    'display': 'flex', 
    'justifyContent': 'center',
    'display': 'block',
    'text-align': 'center',
    'background': 'rgb(0,191,255, .6)'
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
                dbc.NavLink("Create a sample portfolio", href="/page-4", id="page-4-link"),
                dbc.NavLink("Contact Us", href="/page-5", id="page-5-link"),
                dbc.NavLink("FAQ", href="/page-6", id="page-6-link"),
                dbc.NavLink('-------------------------------'),
                dbc.NavLink("Employee Transaction", href="/page-7", id="page-7-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)


# callbacks.present_customer_detail(app)
column_names = []
df_portfolio = pd.DataFrame(columns = column_names)
callbacks.sample_portfolio(app, df_portfolio)

# callbacks.initial_decision(app)
callbacks.login(app)
callbacks.open_account(app)
callbacks.contact_layout(app)
callbacks.present_customer_data(app)

### get info for dropdowns used in journal_data_entry
engine = create_engine('sqlite:///roboinvest.db')
Base = declarative_base()
conn = sqlite3.connect(reference.database)
c = conn.cursor()

''' Getting data from customer and employee tables in the system for the employee login.
These will be dropdowns (so will the transaction type). Peter Koppelman Aug 19, 2020 '''

# Customer name and customer id
c.execute( \
    'SELECT \
        CASE \
            when Middle_initial is Null \
            then First_name || " " || Last_name  \
            else First_name || " " || Middle_initial || " " || Last_name \
        END name, \
        Cust_Id \
    FROM \
        Customer_Master')
cust = c.fetchall()
cust_info = []
for i in range(len(cust)):
    my_dict = dict()
    my_dict['label'] = cust[i][0]
    my_dict['value'] = cust[i][1]
    cust_info.append(my_dict)

## Employee last name and id number
c.execute( \
    'SELECT \
        Last_name, \
        ee_id \
    FROM \
        Employee_Master')
ee = c.fetchall()

ee_info = []
for i in range(len(ee)):
    my_dict = dict()
    my_dict['label'] = ee[i][0]
    my_dict['value'] = ee[i][1]
    ee_info.append(my_dict)


# get valid account numbers for each customer
c.execute( \
    'SELECT \
        customer_master.cust_id, \
        account_master.account_number \
    FROM \
        customer_master \
        Inner Join account_master On account_master.cust_id = Customer_Master.cust_id')
acct = c.fetchall()

acct_info = []
for i in range(len(acct)):
    my_dict = dict()
    my_dict['label'] = acct[i][0]
    my_dict['value'] = acct[i][1]
    acct_info.append(my_dict)

c.close()

callbacks.journal_data_entry(app, cust_info, ee_info)

# sidebar = html.Div([
#     html.Div([
#         html.H4("Robo Investing Tool", className="display-5"),
#         html.Hr(),

#         dbc.Nav(
#             [

#             ],
#             vertical=True,
#             pills=True,
#         ),
#         ], style=SIDEBAR_STYLE,
#     ),
#     html.Div([
#         html.Div([
#         html.H2('The Shore-Koppelman Group'),
#         html.H3('Robo-Investing Tool'),
#             ], style = HEADER_STYLE
#         ),
#         html.Br(),
#         html.Br(),
#         html.H5('Welcome to Robo-Investing! The app for personal investors.',
#             style = TEXT_ALIGN_CENTER ),
#         html.Br(),
#         html.Div([
#         html.Label('Would you like to login or take a tour?'),
#             dcc.Dropdown(
#                 id = 'initial_decision', 
#                 options = [
#                     {'label': 'Login', 'value': '1'},
#                     {'label': 'Take a tour', 'value': '2'}],
#                     style = {'fontsize': 24, 
#                             'width': 200,
#                             'display': 'inline-block',
#                             'position': 'relative',
#                             'left': 2,
#                             'top': 5,
#                             }
#                     ), html.Div(id = 'decision')
#             ], style = TEXT_ALIGN_CENTER
#         )
#     ])
# ])

content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([
    dcc.Location(id="url", refresh = False), sidebar, content
])

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 8)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False, False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 8)]


@app.callback(Output("page-content", "children"), 
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname in ['/', '/page-1']:
        return layout.welcome()
    elif pathname == "/page-2":
        return layout.login()
    elif pathname == "/page-3":
        return layout.open_account(app)
    elif pathname == "/page-4":
        return layout.sample_portfolio_layout(app, df_portfolio)
    elif pathname == "/page-5":
       return layout.contact_layout(app)
    elif pathname == '/page-6':
        return layout.faq()
    elif pathname == '/page-7':
        return layout.journal_data_entry(app, cust_info, ee_info)


if __name__ == "__main__":
    app.run_server(debug=True)
