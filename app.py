from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
from flask_mysqldb import MySQL

load_dotenv()

app = Flask(__name__)

app.config['PERMANENT_SESSION_LIFETIME'] = 3600

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

    if(session):
        return redirect("/home")
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        try:
            user = usuarioModel.autenticarLogin(nome, senha)
            print(f"usuario: {user[0]}")
            if user:
                session['id_usuario'] = user[0]
                return redirect("/home")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    return render_template('login.html')

@app.route("/home", methods=['GET', 'POST'])
def homeUm():
    print(f"usuario: {session}")
    if(session):
        return render_template('index.html')
    return redirect('/login')

@app.route("/clientesVeiculos", methods=['GET', 'POST'])
def clientesVeiculos():
    print(f"sessão: {session}")
    if(session):
        return render_template('clientesVeiculos.html')
    return redirect('/login')

@app.route("/pecas", methods=['GET', 'POST'])
def pecas():
    print(f"sessão: {session}")
    if(session):
        return render_template('pecas.html')
    return redirect('/login')

@app.route("/mecanicosEquipes", methods=['GET', 'POST'])
def mecanicosEquipes():
    print(f"sessão: {session}")
    if(session):
        return render_template('mecanicosEquipes.html')
    return redirect('/login')
    
@app.route("/servicos", methods=['GET', 'POST'])
def servicos():
    print(f"sessão: {session}")
    if(session):
        return render_template('servicos.html')
    return redirect('/login')