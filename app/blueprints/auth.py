# auth-api/app/blueprints/auth.py

from flask import Blueprint, request, jsonify
from app.security import create_token, decode_token
from app.extensions import bcrypt
from app.models import User

# Cria o blueprint para autenticação
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Rota para registrar um novo usuário."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # 1. Validação de entrada
    if not email or not password:
        return jsonify({'message': 'Email e senha são obrigatórios'}), 400

    # 2. Verifica se o usuário já existe
    if User.find_by_email(email):
        return jsonify({'message': 'Email já cadastrado'}), 409

    # 3. Criptografa a senha e cria o novo usuário
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email, hashed_password)
    user.save_to_db()

    return jsonify({'message': 'Usuário registrado com sucesso'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Rota para fazer login e obter um token JWT."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # 1. Validação de entrada
    if not email or not password:
        return jsonify({'message': 'Email e senha são obrigatórios'}), 400

    # 2. Busca o usuário no banco de dados
    user_data = User.find_by_email(email)

    # 3. Valida as credenciais (usuário e senha)
    if not user_data or not bcrypt.check_password_hash(user_data['password'], password):
        return jsonify({'message': 'Credenciais inválidas'}), 401

    # 4. Cria e retorna o token JWT
    token = create_token(user_data['_id'])

    return jsonify({'message': 'Login bem-sucedido', 'access_token': token}), 200

@auth_bp.route('/profile', methods=['GET'])
def protected_route():
    """Rota protegida que requer um token JWT válido."""
    auth_header = request.headers.get('Authorization')

    # 1. Verifica se o cabeçalho de autorização existe
    if not auth_header:
        return jsonify({'message': 'Token de autenticação é obrigatório'}), 401

    # 2. Extrai o token do cabeçalho
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return jsonify({'message': 'Formato de token inválido'}), 401
    token = parts[1]

    # 3. Decodifica o token
    payload = decode_token(token)
    if not payload:
        return jsonify({'message': 'Token inválido ou expirado'}), 401

    # 4. Busca o usuário usando o ID do payload
    user_id = payload.get('sub')
    user_data = User.find_by_id(user_id)

    if not user_data:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    # 5. Retorna os dados do perfil do usuário
    return jsonify({
        'email': user_data['email'],
        'created_at': user_data['created_at']
    }), 200
