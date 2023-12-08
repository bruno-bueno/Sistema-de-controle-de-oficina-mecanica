from flask import Flask, render_template, request, redirect, url_for, session
import os
import hashlib

from model import db, Usuario, Servicos, Pecas, Endereco, Cliente, Veiculo, Equipes, Mecanico, ServicosHasEquipes, ServicosHasMecanicos, OrdemServico, OrdemServicosHasServicos, PecasHasOrdemServicos

app = Flask(__name__)

app.config['PERMANENT_SESSION_LIFETIME'] = 3600

app.secret_key = os.getenv('SECRET_KEY')

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://doadmin:AVNS_OvgSkSeBx7y7gC59WDy@db-mysql-nyc3-96783-do-user-15310791-0.c.db.ondigitalocean.com:25060/oficina_mecanica'

db.init_app(app)

def md5(texto):
    hash_md5 = hashlib.md5()
    hash_md5.update(texto.encode('utf-8'))
    return hash_md5.hexdigest()

@app.route("/")
def home():
    if(session):
        return redirect('/home')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if(session):
        return redirect("/home")
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        try:
            user = Usuario.query.filter_by(nome=nome, senha=md5(senha)).first()
            print("usuario: {user.id_usuario}")
            if user:
                print( "usuario: {user.senha}")
                session['id_usuario'] = user.id_usuario
                return redirect("/home")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    return render_template('login.html')

@app.route("/home", methods=['GET'])
def homeUm():
    print(f"usuario: {session}")
    if(session):
        clientes = Cliente.query.all()
        equipes = Equipes.query.all()
        veiculos = Veiculo.query.all()
        servicos = Servicos.query.all()
        pecas = Pecas.query.all()
        ordensServicos = OrdemServico.query.all()
        return render_template('index.html', clientes = clientes, equipes = equipes, veiculos = veiculos, servicos = servicos, pecas = pecas, ordensServicos = ordensServicos, obterServico = obterServico)
    return redirect('/login')

@app.route("/ordemServicos", methods=['POST'])
def ordemServicos():
    if request.method == 'POST':
        defeito = request.form['defeito']
        dataEmissao = request.form['dataEmissao']
        previsaoEntrega = request.form['previsaoEntrega']
        cliente = int(request.form['cliente'])
        veiculo = request.form['veiculo']
        servico = int(request.form['servico'])
        peca = int(request.form['peca'])
        equipe = int(request.form['equipe'])
        valor = float(request.form['valor'])

        ordemServico = OrdemServico(defeito = defeito, data_emissao = dataEmissao, previsao_entrega = previsaoEntrega, status_ordem = 0, id_cliente = cliente, id_equipes = equipe, id_veiculo = veiculo, valor_cobrado = valor)
        db.session.add(ordemServico)
        db.session.commit()

        ordemServico_id = ordemServico.id_ordem_servicos

        pecasHasOrdemServicos = PecasHasOrdemServicos(pecas_id_pecas = peca, ordem_servicos_id_ordem_servicos = ordemServico_id)
        db.session.add(pecasHasOrdemServicos)
        db.session.commit()

        ordemServicosHasServicos = OrdemServicosHasServicos(ordem_servicos_id_ordem_servicos = ordemServico_id, servicos_id_servicos = servico)
        db.session.add(ordemServicosHasServicos)
        db.session.commit()
        return redirect('/home')
    return redirect('/login')

@app.route("/clientesVeiculos", methods=['GET'])
def clientesVeiculos():
    print(f"sessão: {session}")
    if(session):
        clientes = Cliente.query.all()
        enderecos = Endereco.query.all()
        veiculos = Veiculo.query.all()
        return render_template('clientesVeiculos.html', clientes = clientes, enderecos = enderecos, veiculos = veiculos, obterEndereco = obterEndereco, obterCliente = obterCliente)
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


        return redirect('/clientesVeiculos')
    return redirect('/login')

@app.route("/veiculos", methods=['POST'])
def veiculos():
    print(f"sessão: {session}")
    if(session):
        if request.method == 'POST':
            placa = request.form['placa']
            marca = request.form['marca']
            modelo = request.form['modelo']
            ano = int(request.form['ano'])
            cor = request.form['cor']
            cliente = int(request.form.get('cliente'))

            veiculo = Veiculo(placa = placa, marca = marca, modelo = modelo, ano = ano, cor = cor, id_cliente = cliente)
            db.session.add(veiculo)
            db.session.commit()

            print("teste")

        return redirect('/clientesVeiculos')
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

@app.route("/mecanicosEquipes", methods=['GET'])
def mecanicosEquipes():
    print(f"sessão: {session}")
    if(session):

        servicos = Servicos.query.all()
        equipes = Equipes.query.all()
        mecanicos = Mecanico.query.all()
        return render_template('mecanicosEquipes.html',servicos = servicos, equipes = equipes, mecanicos = mecanicos, obterEspecialidadeEquipe=obterEspecialidadeEquipe, obterEspecialidadeMecanico=obterEspecialidadeMecanico, obterEndereco = obterEndereco, obterMecanico = obterMecanico)
    return redirect('/login')

@app.route("/mecanicos", methods=['POST'])
def mecanicos():
    print(f"sessão: {session}")
    if(session):
        nome = request.form['nome']
        cep = int(request.form['cep'])
        rua = request.form['rua']
        bairro = request.form['bairro']
        numero = int(request.form['numero'])
        servico = int(request.form.get('servico'))
        equipe = int(request.form.get('equipe'))

        endereco = Endereco(cep = cep, rua = rua, bairro = bairro, numero = numero)
        db.session.add(endereco)
        db.session.commit()

        endereco_id = endereco.id_endereco

        mecanico = Mecanico(nome = nome, id_equipe = equipe, id_endereco = endereco_id)
        db.session.add(mecanico)
        db.session.commit()

        mecanico_id = mecanico.id_mecanicos

        especialidade = ServicosHasMecanicos(servicos_id_servicos = servico, mecanicos_id_mecanicos = mecanico_id)
        db.session.add(especialidade)
        db.session.commit()
        
        return redirect('/mecanicosEquipes')
    return redirect('/login')

@app.route("/equipes", methods=['POST'])
def equipes():
    print(f"sessão: {session}")
    if(session):
        nome = request.form['nome']
        servico = int(request.form.get('servico'))

        equipes = Equipes(nome=nome)
        db.session.add(equipes)
        db.session.commit()

        equipes_id = equipes.id_equipes

        especialidade = ServicosHasEquipes(servicos_id_servicos = servico, equipes_id_equipes = equipes_id)
        db.session.add(especialidade)
        db.session.commit()

        return redirect('/mecanicosEquipes')
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

@app.route("/usuarios", methods=['GET'])
def usuarios():
    print(f"usuario: {session}")
    if(session):
        print(f"usuario2: {session.get('id_usuario')}")
        usuarios = Usuario.query.all()
        return render_template('usuarios.html', usuarios = usuarios)
    return redirect('/login')

@app.route("/addUsuarios", methods=['POST'])
def addUsuarios():
    print(f"usuario: {session}")
    if(session):
        if request.method == 'POST':
            nome = request.form['nome']
            senha = request.form['senha']

            usuario = Usuario(nome=nome, senha=senha)
            db.session.add(usuario)
            db.session.commit()

        return redirect('/usuarios')
    return redirect('/login')

@app.route("/metasFinalizadas", methods=['GET'])
def metasFinalizadas():
    print(f"usuario: {session}")
    if(session):
        print(f"usuario2: {session.get('id_usuario')}")
        clientes = Cliente.query.all()
        equipes = Equipes.query.all()
        veiculos = Veiculo.query.all()
        servicos = Servicos.query.all()
        pecas = Pecas.query.all()
        ordensServicos = OrdemServico.query.all()
        return render_template('metasFinalizadas.html', clientes = clientes, equipes = equipes, veiculos = veiculos, servicos = servicos, pecas = pecas, ordensServicos = ordensServicos, obterServico = obterServico)
    return redirect('/login')

@app.route("/statusOrdem", methods=['POST'])
def alterarStatus():
    print("chegou")
    valor = int(request.form.get('valor'))
    id = int(request.form.get('id'))
    ordem = OrdemServico.query.filter_by(id_ordem_servicos = id).first()
    if ordem:
        ordem.status_ordem = valor
        db.session.commit()
    return redirect('/home')

@app.route("/sair", methods=['GET'])
def sair():
    print("veio")
    session.clear()
    return redirect('/login')

def obterEspecialidadeEquipe(id_equipe):
    servicoId = ServicosHasEquipes.query.filter_by( equipes_id_equipes = id_equipe ).with_entities(ServicosHasEquipes.servicos_id_servicos).first()
    if servicoId is not None:
        servico = Servicos.query.filter_by(id_servicos = servicoId[0]).first()
        print(servicoId[0])
        if servico:
            print(servico)
            return servico.nome
    return 'Serviço não encontrado'

def obterEspecialidadeMecanico(id_mecanico):
    servicoId = ServicosHasMecanicos.query.filter_by(mecanicos_id_mecanicos=id_mecanico).with_entities(ServicosHasMecanicos.servicos_id_servicos).first()
    if servicoId is not None:
        servico = Servicos.query.filter_by(id_servicos=servicoId[0]).first()
        print(servicoId[0])
        if servico:
            print(servico)
            return servico.nome
    return 'Serviço não encontrado'

def obterEndereco(id_endereco):
    endereco = Endereco.query.filter_by( id_endereco = id_endereco ).first()
    if endereco:
        return endereco
    return 'Endereço não encontrado'

def obterMecanico(id_equipe):
    mecanicos = Mecanico.query.filter_by( id_equipe = id_equipe ).first()
    if mecanicos:
        return mecanicos.nome
    return 'Mecânicos não encontrado'

def obterCliente(id_cliente):
    cliente = Cliente.query.filter_by( id_clientes = id_cliente ).first()
    if cliente:
        return cliente.nome
    return 'Cliente não encontrado'

def obterServico(id_ordem_servicos):
    servicoId = OrdemServicosHasServicos.query.filter_by(ordem_servicos_id_ordem_servicos=id_ordem_servicos).with_entities(OrdemServicosHasServicos.servicos_id_servicos).first()
    if servicoId is not None:
        servico = Servicos.query.filter_by(id_servicos=servicoId[0]).first()
        if servico:
            print(servico)
            return servico
    return 'Serviço não encontrado'

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')