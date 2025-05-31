from flask import Flask


def create_app():
    app = Flask(__name__)
    # app.config['SECRET_KEY'] = 'fc089b9218301ad987914c53481bff04'

    with app.app_context():
        # Initialize the database
        from .database import init_db
        init_db()
    from .routes import bp
    app.register_blueprint(bp)

    return app