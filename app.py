# App2.py - front end using dash bootstrap components
# July 2, 2020 Peter Koppelman

import dash as dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from apps import layout, callbacks, reference
import pandas as pd

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

sidebar = html.Div(
    [
        html.H4("Robo Investing Tool", className="display-5"),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("Welcome", href="/page-1", id="page-1-link"),
                dbc.NavLink("Client Login", href="/page-2", id="page-2-link"),
                dbc.NavLink("Open an account", href="/page-3", id="page-3-link"),
                dbc.NavLink("Create a sample portfolio", href="/page-4", id="page-4-link"),
                dbc.NavLink("Contact Us", href="/page-5", id="page-5-link"),
                dbc.NavLink("FAQ", href="/page-6", id="page-6-link"),
                dbc.NavLink('-------------------------------'),
                dbc.NavLink("Employee Login", href="/page-7", id="page-7-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

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
    if pathname == '/page-1':
        return layout.welcome()
    elif pathname == "/page-2":
        return layout.client_login()
    elif pathname == "/page-3":
        return layout.open_account(app)
    elif pathname == "/page-4":
        return layout.sample_portfolio_layout(app, df_portfolio)
    elif pathname == "/page-5":
       return layout.contact_layout(app)
    elif pathname == '/page-6':
        return layout.faq()
    elif pathname == '/page-7':
        return layout.journal_data_entry(app)


callbacks.present_customer_data(app)
callbacks.present_customer_detail(app)

callbacks.client_login(app)
callbacks.journal_data_entry(app)
callbacks.open_account(app)
callbacks.contact_layout(app)

column_names = []
df_portfolio = pd.DataFrame(columns = column_names)
callbacks.sample_portfolio(app, df_portfolio)


if __name__ == "__main__":
    app.run_server(debug=True)
