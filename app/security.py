# auth-api/app/security.py

import jwt
from datetime import datetime, timedelta
from flask import current_app

def create_token(user_id):
    """
    Cria um token JWT para o usuário especificado.
    O token expira em 1 hora.
    """
    payload = {
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow(),
        'sub': str(user_id)  # O 'sub' (subject) do token é o ID do usuário
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def decode_token(token):
    """
    Decodifica um token JWT e retorna o payload.
    Retorna None em caso de token inválido ou expirado.
    """
    try:
        # Tenta decodificar o token
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # O token expirou
        return None
    except jwt.InvalidTokenError:
        # O token é inválido
        return None
