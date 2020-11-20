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


    # app.debug = True



    with app.app_context():


        @app.after_request
        def add_header(response):
            """
            Add headers to both force latest IE rendering engine or Chrome Frame,
            and also to cache the rendered page for 10 minutes.
            """
            response.headers['X-UA-Compatible'] = "IE=Edge,chrome=1"
            response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate, public, max-age=0"
            response.headers["Expires"] = 0
            response.headers["Pragma"] = "no-cache"
            return response
        
        app.register_blueprint(page)
        # app.register_blueprint(user)
        # extensions(app)
        # authentication(app, User)
        
        from .plotlydash.dashboard import create_dashboard
        dashapp = create_dashboard(server=app)

        return app
