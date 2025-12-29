from dash import dcc, html, callback ,Input, Output, State
import dash 
import dash_bootstrap_components as dbc


from UILayer.DashAppUtilities import Send_Query

dash.register_page(
    __name__,
    path="/chatBot",
    name="Educational Chat Assistant"
    )


layout = dbc.Container(
    [
        # ---------- PAGE TITLE ----------
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Educational Chat Assistant",
                    className="text-start mt-3 mb-4",
                    style={"font-size": "35px"}
                ),
                width=12
            )
        ),

          # ---------- CHAT WINDOW ----------
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Conversation",
                            className="fw-semibold"
                        ),
                        dbc.CardBody(
                            [
                                
                                dcc.Markdown(
                                    id="chat-output",
                                    children="*Ask a question to begin the conversation.*",
                                    style={
                                        "height": "420px",
                                        "overflowY": "auto",
                                        "whiteSpace": "pre-wrap"
                                    }
                                )
                            ],
                            style={"backgroundColor": "#fafafa"}
                        )
                    ],
                    className="shadow-sm"
                ),
                width=12
            )
        ),

        # ---------- USER INPUT ----------
        dbc.Row(
            [
                dbc.Col(
                    dcc.Textarea(
                        id="chat-input",
                        placeholder="Type your question here...",
                        style={
                            "width": "100%",
                            "height": "90px",
                            "resize": "none"
                        }
                    ),
                    width=10
                ),
                dbc.Col(
                    dbc.Button(
                        "Send",
                        id="btn-send",
                        color="primary",
                        className="w-100 h-100",
                        n_clicks=0
                    ),
                    width=2
                )
            ],
            className="mt-3"
        )

    ],
    fluid=True,
    className="p-4"
)


@callback(
    Output("chat-output", "children"),
    Input("btn-send", "n_clicks"),
    State("chat-input", "value"),
    prevent_initial_call=True
)
def update_chat(n_clicks, user_input):
    if n_clicks > 0 and user_input:
        answer = Send_Query(user_input)
        chat_history = f"User: {user_input}\n\nAssistant: {answer}\n\n"
        return chat_history
    return dash.no_update