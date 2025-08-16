
import os

class Config:
    """Classe base para as configurações da aplicação."""

    MONGO_URI = os.environ.get("MONGO_URI")

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
