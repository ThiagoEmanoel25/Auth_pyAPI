# auth-api/app/extensions.py

from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

# Instâncias globais das extensões
mongo = PyMongo()
bcrypt = Bcrypt()
