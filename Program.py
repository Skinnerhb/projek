import dash

external_stylesheets = ['bWLwgP.css']
program = dash.Dash(__name__,external_stylesheets = external_stylesheets)
server = program.server
program.config.suppress_callback_exceptions=True