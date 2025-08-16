const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

// Carrega as variáveis de ambiente do arquivo .env
require('dotenv').config();

const app = express();
app.use(express.json());

// Conecta ao MongoDB
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/authdb')
  .then(() => console.log('Conectado ao MongoDB com sucesso!'))
  .catch(err => console.error('Erro de conexão com o MongoDB:', err));

// ## Modelo de Usuário
// Usamos "email" como identificador único para o login
const UserSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true, lowercase: true },
  password: { type: String, required: true }
});
const User = mongoose.model('User', UserSchema);

// ## Rotas de Autenticação

// Rota de Registro
app.post('/register', async (req, res) => {
  try {
    const { email, password } = req.body;

    // 1. Validação de entrada
    if (!email || !password) {
      return res.status(400).json({ message: 'Email e senha são obrigatórios.' });
    }

    // 2. Verifica se o usuário já existe
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ message: 'Este email já está em uso.' });
    }

    // 3. Criptografa a senha e salva o novo usuário
    const hashedPassword = await bcrypt.hash(password, 10);
    const user = new User({ email, password: hashedPassword });
    await user.save();

    res.status(201).json({ message: 'Usuário registrado com sucesso.' });
  } catch (error) {
    console.error('Erro ao registrar usuário:', error);
    res.status(500).json({ error: 'Erro no servidor.', details: error.message });
  }
});

// Rota de Login
app.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    // 1. Validação de entrada
    if (!email || !password) {
      return res.status(400).json({ message: 'Email e senha são obrigatórios.' });
    }

    // 2. Busca o usuário pelo email
    const user = await User.findOne({ email });

    // 3. Validação de credenciais (usuário e senha)
    if (!user || !await bcrypt.compare(password, user.password)) {
      return res.status(401).json({ message: 'Credenciais inválidas.' });
    }

    // 4. Cria o token JWT
    const token = jwt.sign(
      { userId: user._id, email: user.email },
      process.env.JWT_SECRET || 'uma_chave_secreta_padrao_muito_segura',
      { expiresIn: '1h' }
    );

    res.json({ access_token: token });
  } catch (error) {
    console.error('Erro no processo de login:', error);
    res.status(500).json({ error: 'Erro no servidor.', details: error.message });
  }
});

// ## Inicialização do Servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Servidor rodando na porta ${PORT}`));