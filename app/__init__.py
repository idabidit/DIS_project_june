from flask import Flask


def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config['SECRET_KEY'] = 'fc089b9218301ad987914c53481bff04'

    from .routes import bp

    app.register_blueprint(bp)

    return app
