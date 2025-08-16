
from .extensions import mongo
import datetime
from bson.objectid import ObjectId

class User:
    """
    Modelo de dados para um usuário.
    Mapeia para um documento na coleção 'users' do MongoDB.
    """
    def __init__(self, email, password):
        """Inicializa um novo objeto User."""
        self.email = email
        self.password = password
        self.created_at = datetime.datetime.utcnow()

    def save_to_db(self):
        """Salva o usuário no banco de dados."""
        user_data = {
            'email': self.email,
            'password': self.password,
            'created_at': self.created_at
        }
        mongo.db.users.insert_one(user_data)

    @staticmethod
    def find_by_email(email):
        """
        Busca um usuário no banco de dados pelo email.
        Retorna o documento encontrado ou None se não existir.
        """
        return mongo.db.users.find_one({'email': email})

    @staticmethod
    def find_by_id(user_id):
        """
        Busca um usuário pelo seu ID.
        Retorna o documento encontrado ou None.
        """
        return mongo.db.users.find_one({'_id': ObjectId(user_id)})
