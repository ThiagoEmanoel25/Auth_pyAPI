from flask import Flask
from .config import Config
from .extensions import mongo, bcrypt
from .blueprints.auth import auth_bp

def create_app(config_class=Config):
    """
    Função de fábrica da aplicação.
    Cria e configura uma instância do app Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa as extensões com a instância do app
    mongo.init_app(app)
    bcrypt.init_app(app)

    # Registra os Blueprintss
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app