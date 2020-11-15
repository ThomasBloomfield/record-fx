from flask import Flask

from recordcurrency.blueprints.page import page


def create_app(debug=True):
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    with app.app_context():

        app.register_blueprint(page)
        # app.register_blueprint(user)
        # extensions(app)
        # authentication(app, User)
        
        from .plotlydash.dashboard import create_dashboard
        dashapp = create_dashboard(server=app)

        return app
