"""
    Routing for the home page, '/'

    Attributes
    ----------
    app : flask.app.Flask
        The flask app, running the API
"""


def routes(app):
    """
        '/' route, presenting a simple welcoming message. Has 
        no functionality. Mostly exists just to test the service.

        Returns
        -------
        msg : dict
            A message to welcome the user
    """
    @app.route('/')
    def index():
        msg = {"message": "Smart Home"}
        return msg, 200
