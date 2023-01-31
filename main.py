from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
import os
import openai

# load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# define layout
app.layout = dbc.Container([
    dbc.Row([dbc.Col([html.H1("Customer Chatbot")], width=12)]),

    dbc.Row([
        dbc.Col([
            html.H4("Ask our chatbot a question:"),
            dcc.Input(id='text-input',
                      placeholder='Type a question...', type='text'),
            dbc.Button("Ask", color="primary", id='ask-button')], width='auto')
    ], align='end', justify='left'),
    html.Br(),
    html.Div(id='chatbot-answer')]
)

# define callbacks


@ app.callback(
    Output(component_id='chatbot-answer', component_property='children'),
    Input(component_id='text-input', component_property='value'),
    Input(component_id='ask-button', component_property='n_clicks')
)
def update_output_div(user_text, click):
    if click:
        # clean input text
        # feed to openai chat gpt api
        openai_response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(user_text),
            temperature=0.6
        )
        # clean response
        return f"Chatbot: {openai_response['choices'][0].text}"

# helper functions


def generate_prompt(user_question):
    return f"""Act like you are a customer service agent at a IT company.
    Respond as if you were talking to a 3rd grader. Please write at least 3 sentences and include step by step instructions.
    
    Example question: How do I reset my password?
    Answer:
    1. Go to the website
    2. Click on the login button
    3. Click on the forgot password link

    Example question: How do I fix my computer?
    Answer:
    1. Turn off your computer
    2. Unplug the power cord
    3. Wait 30 seconds
    4. Plug the power cord back in
    
    My question is: {user_question}?
    Answer:"""


if __name__ == '__main__':
    app.run_server()
