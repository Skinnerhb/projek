import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from Program import program
from testing1 import layout1, layout2
import testing2


program.layout = html.Div([
    dcc.Location(id='url',pathname='/api/login', refresh = False),
    html.Div(id = 'patherr')
    ])

@program.callback(
    Output('patherr','children'),
    [Input('url','pathname')]
    )
def caller(pathname):
    if pathname == '/api/login':
        return layout1
    if pathname == '/api/api2':
        return layout2



if __name__ == '__main__':
    program.run_server(debug=True)

