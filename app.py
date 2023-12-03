from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
import hashlib

from model import db, Usuario, Servicos, Pecas, Endereco, Cliente

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

@app.route("/clientesVeiculos", methods=['GET'])
def clientesVeiculos():
    print(f"sessão: {session}")
    if(session):
        clientes = Cliente.query.all()
        enderecos = Endereco.query.all()
        return render_template('clientesVeiculos.html', clientes = clientes, enderecos = enderecos)
    return redirect('/login')

@app.route("/clientes", methods=['POST'])
def clientes():
    print(f"sessão: {session}")
    if(session):
        if request.method == 'POST':
            nome = request.form['nome']
            cep = int(request.form['cep'])
            rua = request.form['rua']
            bairro = request.form['bairro']
            numero = int(request.form['numero'])

            endereco = Endereco(cep = cep, rua = rua, bairro = bairro, numero = numero)
            db.session.add(endereco)
            db.session.commit()

            endereco_id = endereco.id_endereco

            cliente = Cliente(nome=nome, id_endereco=endereco_id)
            db.session.add(cliente)
            db.session.commit()
            print("teste")

        return render_template('clientesVeiculos.html')
    return redirect('/login')

@app.route("/pecas", methods=['GET', 'POST'])
def pecas():
    print(f"sessão: {session}")
    if(session):
        if request.method == 'POST':
            nome_da_peca = request.form['nome_da_peca']
            marca = request.form['marca']
            valor = float(request.form['valor'])

            pecas = Pecas(nome_da_peca=nome_da_peca, marca=marca, valor=valor)
            db.session.add(pecas)
            db.session.commit()
            print("teste")
        
        pecas = Pecas.query.all()
        return render_template('pecas.html', pecas = pecas)
    return redirect('/login')

@app.route("/mecanicosEquipes", methods=['GET', 'POST'])
def mecanicosEquipes():
    print(f"sessão: {session}")
    if(session):
        return render_template('mecanicosEquipes.html')
    return redirect('/login')
    
@app.route("/servicos", methods=['GET', 'POST'])
def servicos():
    print("sessão: {session}")
    if(session):
        if request.method == 'POST':
            nome = request.form['nome']
            descricao = request.form['descricao']
            valor = float(request.form['valor'])

            servico = Servicos(nome=nome, descricao=descricao, valor=valor)
            db.session.add(servico)
            db.session.commit()
            print("teste")

        servicos = Servicos.query.all()
        return render_template('servicos.html', servicos = servicos)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)