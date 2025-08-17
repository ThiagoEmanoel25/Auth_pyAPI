#Auth-api: API de Autenticação em Flask com MongoDB#


Este é um projeto de API de autenticação simples e robusto, construído com o framework Flask e o banco de dados NoSQL MongoDB. A API oferece endpoints para registro, login e acesso a rotas protegidas usando tokens JWT (JSON Web Tokens).

🛠️ Tecnologias Utilizadas
Python 3.10+

*Flask: Um micro-framework web para Python.

*Flask-PyMongo: Integração com o banco de dados MongoDB.

*Flask-Bcrypt: Para criptografia segura de senhas.

*PyJWT: Para geração e verificação de tokens JWT.

*python-dotenv: Para gerenciar variáveis de ambiente.

📂 Estrutura do Projeto
O projeto segue uma estrutura modular, com responsabilidades bem definidas para cada arquivo e pasta:

auth-api/
├── .env                  # Variáveis de ambiente (excluído do git)
├── .env.example          # Modelo de variáveis de ambiente
├── requirements.txt      # Dependências do Python
├── run.py                # Ponto de entrada da aplicação
│
├── app/                  # Módulo principal da aplicação
│   ├── __init__.py       # Função de fábrica da aplicação
│   ├── config.py         # Configurações do app
│   ├── extensions.py     # Inicialização das extensões
│   ├── models.py         # Modelos de dados do MongoDB
│   ├── security.py       # Lógica de criação/decodificação de tokens JWT
│   │
│   └── blueprints/       # Rotas organizadas
│       └── auth.py       # Rotas de autenticação (registro, login, perfil)

🚀 Instalação e Uso
1. Clone o Repositório
Primeiro, clone este repositório para sua máquina local usando o Git:

git clone git@github.com:ThiagoEmanoel25/Auth_pyAPI
cd Auth_pyAPI

2. Configure as Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto e preencha-o com suas informações. Use o arquivo .env.example como guia:

# .env.example
MONGO_URI=
JWT_SECRET_KEY=
PORT=

3. Instale as Dependências
Crie um ambiente virtual (recomendado) e instale todas as dependências listadas no requirements.txt:

python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

4. Inicie o Servidor
Com as dependências instaladas, você pode iniciar o servidor Flask:

python run.py

O servidor estará rodando em http://localhost:5000.

🚦 Endpoints da API
Você pode testar os endpoints usando o Postman ou qualquer outro cliente HTTP.

POST /api/auth/register
Registra um novo usuário no banco de dados.

Corpo da Requisição:

{
  "email": "teste@example.com",
  "password": "uma_senha_muito_segura"
}

Resposta de Sucesso (201 Created):

{
  "message": "Usuário registrado com sucesso"
}

POST /api/auth/login
Autentica um usuário e retorna um token de acesso JWT.

Corpo da Requisição:

{
  "email": "teste@example.com",
  "password": "uma_senha_muito_segura"
}

Resposta de Sucesso (200 OK):

{
  "message": "Login bem-sucedido",
  "access_token": "seu_token_jwt_longo_aqui"
}

GET /api/auth/profile
Endpoint protegido. Retorna os dados do perfil do usuário se o token JWT for válido.

Cabeçalho da Requisição:

Authorization: Bearer <seu_token_jwt_longo_aqui>

Resposta de Sucesso (200 OK):

{
  "email": "teste@example.com",
  "created_at": "2024-05-18T12:00:00.000Z"
}
