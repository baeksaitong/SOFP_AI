from flask import Flask
from .config import Config
from .routes import routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 라우팅 모듈 등록
    app.register_blueprint(routes)

    return app
