import dash

external_stylesheets = ['bWLwgP.css']
program = dash.Dash(__name__,external_stylesheets = external_stylesheets)
server = program.server
program.config.suppress_callback_exceptions=True
program.scripts.config.serve_locally = True
program.css.serve_locally = True