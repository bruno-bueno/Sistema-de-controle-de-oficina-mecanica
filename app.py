from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
from flask_mysqldb import MySQL

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'oficina_mecanica'

mysql = MySQL(app) 

app.secret_key = os.getenv('SECRET_KEY')

@app.route("/")
def home():
    return "Hello, World!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    from model import Usuarios 
    usuarioModel = Usuarios()  

    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        user = usuarioModel.autenticarLogin(nome, senha)

        if user:
            session['id_usuario'] = user['id_usuario']
            return redirect(url_for('dashboard'))

    return render_template('login.html')
