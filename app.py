from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
import hashlib

from model import db, Usuario

app = Flask(__name__)

app.config['PERMANENT_SESSION_LIFETIME'] = 3600

app.secret_key = os.getenv('SECRET_KEY')

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/oficina_mecanica"

db.init_app(app)

def md5(texto):
    hash_md5 = hashlib.md5()
    hash_md5.update(texto.encode('utf-8'))
    return hash_md5.hexdigest()

@app.route("/")
def home():
    return "Hello, World!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    # usuarioModel = Usuarios()

    if(session):
        return redirect("/home")
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        try:
            user = Usuario.query.filter_by(nome=nome, senha=md5(senha)).first()
            print(f"usuario: {user.id_usuario}")
            if user:
                print(f"usuario: {user.senha}")
                session['id_usuario'] = user.id_usuario
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
        if request.method == 'POST':
            if request.form['servicos']:
                nome = request.form['nome']
                print(f"teste")


        return render_template('servicos.html')
    return redirect('/login')