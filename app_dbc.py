# App2.py - front end using dash bootstrap components
# July 2, 2020 Peter Koppelman

import dash as dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import contact_us_dbc as contact_us
import welcome_dbc as welcome
import calc_portfolio_dbc as calc_portfolio


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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
        html.P("Robo Investing Tool", className="display-4"),
        html.Hr(),
        # html.P(
            # "Robo Investing Tool", className="lead"
        # ),
        dbc.Nav(
            [
                dbc.NavLink("Welcome", href="/page-1", id="page-1-link"),
                dbc.NavLink("Create a portfolio", href="/page-2", id="page-2-link"),
                dbc.NavLink("Contact Us", href="/page-3", id="page-3-link"),
                dbc.NavLink("FAQ", href="/page-4", id="page-4-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), 
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return welcome.welcome

    elif pathname == "/page-2":
        return calc_portfolio.get_data

    elif pathname == "/page-3":
        return contact_us.email

    elif pathname == '/page-4':
        return html.P('Welcome to the FAQ Page')


if __name__ == "__main__":
    app.run_server(debug=True)

