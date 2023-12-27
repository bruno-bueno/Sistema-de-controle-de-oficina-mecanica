from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60))
    senha = db.Column(db.String(50))

class Servicos(db.Model):
    __tablename__ = 'servicos'
    id_servicos = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60))
    descricao = db.Column(db.String(60))
    valor = db.Column(db.Float)

class Cliente(db.Model): 
    __tablename__ = 'clientes' 
    id_clientes = db.Column(db.Integer, primary_key=True) 
    nome = db.Column(db.String(60)) 
    id_endereco = db.Column(db.Integer, db.ForeignKey('endereco.id_endereco'))

class Endereco(db.Model): 
    __tablename__ = 'endereco' 
    id_endereco = db.Column(db.Integer, primary_key=True) 
    cep = db.Column(db.Integer)
    rua = db.Column(db.String(40)) 
    bairro = db.Column(db.String(30))
    numero = db.Column(db.Integer)
    
class Veiculo(db.Model): 
    __tablename__ = 'veiculos' 
    id_veiculos = db.Column(db.Integer, primary_key=True) 
    placa = db.Column(db.String(10))
    marca = db.Column(db.String(30)) 
    modelo = db.Column(db.String(50)) 
    ano = db.Column(db.Integer) 
    cor = db.Column(db.String(20)) 
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_clientes'))

class Mecanico(db.Model): 
    __tablename__ = 'mecanicos' 
    id_mecanicos = db.Column(db.Integer, primary_key=True) 
    nome = db.Column(db.String(60)) 
    id_equipe = db.Column(db.Integer, db.ForeignKey('equipes.id_equipes'))
    id_endereco = db.Column(db.Integer, db.ForeignKey('endereco.id_endereco'))

class Equipes(db.Model): 
    __tablename__ = 'equipes' 
    id_equipes = db.Column(db.Integer, primary_key=True) 
    nome = db.Column(db.String(30)) 

class OrdemServico(db.Model): 
    __tablename__ = 'ordem_servicos' 
    id_ordem_servicos = db.Column(db.Integer, primary_key=True) 
    defeito = db.Column(db.String(50)) 
    data_emissao = db.Column(db.Date) 
    previsao_entrega = db.Column(db.Date) 
    status_ordem = db.Column(db.SmallInteger) 
    valor_cobrado = db.Column(db.Float)
    id_equipes = db.Column(db.Integer, db.ForeignKey('equipes.id_equipes'))
    id_veiculo = db.Column(db.Integer, db.ForeignKey('veiculos.id_veiculos'))

class ServicosHasEquipes(db.Model): 
    __tablename__ = 'servicos_has_equipes' 
    servicos_id_servicos = db.Column(db.Integer, db.ForeignKey('servicos.id_servicos'), primary_key=True) 
    equipes_id_equipes = db.Column(db.Integer, db.ForeignKey('equipes.id_equipes'), primary_key=True)

class ServicosHasMecanicos(db.Model): 
    __tablename__ = 'servicos_has_mecanicos' 
    servicos_id_servicos = db.Column(db.Integer, db.ForeignKey('servicos.id_servicos'), primary_key=True) 
    mecanicos_id_mecanicos = db.Column(db.Integer, db.ForeignKey('mecanicos.id_mecanicos'), primary_key=True)

class Pecas(db.Model): 
    __tablename__ = 'pecas' 
    id_pecas = db.Column(db.Integer, primary_key=True) 
    nome_da_peca = db.Column(db.String(50))
    marca = db.Column(db.String(50))
    valor = db.Column(db.Float)

class PecasHasOrdemServicos(db.Model): 
    __tablename__ = 'pecas_has_ordem_servicos' 
    pecas_id_pecas = db.Column(db.Integer, db.ForeignKey('pecas.id_pecas'), primary_key=True)
    ordem_servicos_id_ordem_servicos = db.Column(db.Integer, db.ForeignKey('ordem_servicos.id_ordem_servicos'), primary_key=True)
    quantidade = db.Column(db.Integer) 

class OrdemServicosHasServicos(db.Model): 
    __tablename__ = 'ordem_servicos_has_servicos' 
    ordem_servicos_id_ordem_servicos = db.Column(db.Integer, db.ForeignKey('ordem_servicos.id_ordem_servicos'), primary_key=True)
    servicos_id_servicos = db.Column(db.Integer, db.ForeignKey('servicos.id_servicos'), primary_key=True)
    quantidade = db.Column(db.Integer) 