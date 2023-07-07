import dash
import dash_bootstrap_components as dbc
import dash_auth


# Set login credentials
USERNAME_PASSWORD_PAIRS = [['data','analyst']]

# Establish dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions = True,
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    )

# Establish authorization login details
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
    
# Establish serever
server = app.server
