
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

email = html.Div(
        [ 
            dbc.Form(
            [
                dbc.FormGroup(
                    [
                    dbc.Label('To send us a comment please fill out the information below'),
                    html.Br(),
                    dbc.Label('Name:'),
                    dbc.Input(
                        type = 'value',
                        id = 'name',
                        minLength = 3,
                        maxLength = 100,
                        valid = True,
                        style = {'width': 400}
                        ),
                    ],
                ),
                dbc.FormGroup(
                    [
                        dbc.Label('Email address:'),
                        dbc.Input(
                            type="value", 
                            id='email-addr', 
                            minLength = 5,
                            maxLength = 30,
                            valid = True,
                            style = {'width': 400}
                        ),
                    ],
                ),
                dbc.FormGroup(
                    [
                        html.Br(),
                        html.Br(),
                        dbc.Label('Please type your comment below:'),
                        html.Br(),
                        dbc.Label('Minimum 10 characters, maximum 1,000 characters'),
                        dbc.Textarea(
                            id = 'comment',
                            maxLength = 1000,
                            required = True,
                            rows = 10,
                            spellCheck = True,
                            valid = True
                        ),
                    ],
                ),
            dbc.Button('Submit',
                id = 'submit-email',
                color = 'primary',
                n_clicks = 0
            ),
        ],
    ), html.Div(id = 'email-message')
])


@app.callback(
    [Output('email-message', 'children')],
    [Input('submit-email', 'n_clicks')],
    [State('name', 'value'),
    State('email-addr', 'value'),
    State('comment', 'value')]
)

def on_button_click(n_clicks, test_name, email_addr, test_comment):
    if n_clicks is None:
        print('n clicks is 0')
    else:
        print('n_clicks is not 0')

    print('in sendmail function')
    msg = MIMEMultipart()
    msg["From"] = email_addr
    msg["To"] = 'pkoppelman@yahoo.com'
    msg["Subject"] = "Robo Investing Question"
    body = MIMEText('This is a test of the robo investing email system')
    msg.attach(body)

    ctype, encoding = mimetypes.guess_type(email_reference.filetosend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(email_reference.filetosend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(email_reference.filetosend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(email_reference.filetosend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(email_reference.filetosend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
   # attachment.add_header("Content-Disposition", "attachment", filename=email_reference.filetosend)
    # msg.attach(attachment)

    # Send the email - if you get an error that says Username and Password not accepted, please go to the 
    # gmail account that is sending the email and choose 'Less secure app access'. Gmail does not like
    # smtplib - PK March 25, 2020
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email_reference.emailfrom, email_reference.password)
        server.sendmail(email_reference.emailfrom, email_reference.distribution_list, msg.as_string())
        server.close()
        message = True
    except:
        message = False

    return message











   # email_input = dbc.FormGroup(
    #     [
    #         html.Br(),
    #         html.Br(),
    #         dbc.Label('Name:'),
    #         dbc.Input(
    #             type = 'text',
    #             id = 'name',
    #             placeholder = 'Enter your name here',
    #             minLength = 3,
    #             maxLength = 100,
    #             valid = True,
    #             style = {'width': 400}
    #             ),
    #         html.Br(),
    #         dbc.Label('To contact us please enter you email address below:'),
    #         dbc.Input(
    #                 type="email", 
    #                 id='email-addr', 
    #                 placeholder="Enter email address here",
    #                 minLength = 5,
    #                 maxLength = 30,
    #                 valid = True,
    #                 style = {'width': 400}
    #             ),
    #     ], inline = True,
    # )

    # comment = dbc.FormGroup(
    #     [
    #         html.Br(),
    #         html.Br(),
    #         dbc.Label('Please type your comment below:', html_for="comment"),
    #         html.Br(),
    #         dbc.Label('Minimum 10 characters, maximum 1,000 characters'),
    #         dbc.Textarea(
    #             maxLength = 1000,
    #             required = True,
    #             rows = 10,
    #             spellCheck = True,
    #             title = 'enter your comments here',
    #             valid = True
    #             )
    #     ]
    # )

    # email = html.Div(














# email = (
#     [html.Div('To contact us please enter the information below:'),
#         html.Br(),
#             html.Div(
#             [ 
#                 dbc.Form(
#                 [
#                     dbc.FormGroup(
#                         [
#                             dbc.Label('To send us a comment please fill out the information below'),
#                             html.Br(),
#                             dbc.Label('Name:'),
#                             dbc.Input(
#                                 type = 'text',
#                                 id = 'name',
#                                 minLength = 3,
#                                 maxLength = 100,
#                                 valid = True,
#                                 style = {'width': 400}
#                             ),
#                         ]),
#                     dbc.FormGroup(
#                         [
#                             dbc.Label('Email address:'),
#                             dbc.Input(
#                                 type="email", 
#                                 id='email-addr', 
#                                 minLength = 5,
#                                 maxLength = 30,
#                                 valid = True,
#                                 style = {'width': 400}
#                             ),
#                         ]),
#                     dbc.FormGroup(
#                         [
#                             html.Br(),
#                             html.Br(),
#                             dbc.Label('Please type your comment below:', html_for="comment"),
#                             html.Br(),
#                             dbc.Label('Minimum 10 characters, maximum 1,000 characters'),
#                             dbc.Textarea(
#                                 # type = 'text',
#                                 id = 'comment',
#                                 maxLength = 1000,
#                                 required = True,
#                                 rows = 10,
#                                 spellCheck = True,
#                                 valid = True
#                             ),
#                         ]),
#                 ]),
#             ],
#         ),
#     ],
# )

# buttons = html.Div(
#     [
#     dbc.Button('Submit',
#         id = 'submit-button',
#         color = 'primary'
#         ),
#     html.Span(id="output", style={"vertical-align": "middle"}),
#     ]
# )
