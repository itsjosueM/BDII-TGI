from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, Numeric, ForeignKey, Table
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Associação Pessoa <-> Endereco
pessoa_endereco = Table(
    "pessoa_endereco", Base.metadata,
    Column("id_pessoa", Integer, ForeignKey("pessoa.id_pessoa"), primary_key=True, autoincrement=True),
    Column("id_endereco", Integer, ForeignKey("endereco.id_endereco"), primary_key=True),
    Column("id_tipo_endereco", Integer, ForeignKey("tipo_endereco.id_tipo_endereco"))
)

# Associação Imovel <-> Caracteristica
imovel_caracteristica = Table(
    "imovel_caracteristica", Base.metadata,
    Column("id_imovel", Integer, ForeignKey("imovel.id_imovel"), primary_key=True, autoincrement=True),
    Column("id_caracteristica", Integer, ForeignKey("caracteristica.id_caracteristica"), primary_key=True),
    Column("detalhe", String(100))
)

# ===== Tipos e Status =====
class TipoPessoa(Base):
    __tablename__ = "tipo_pessoa"
    id_tipo_pessoa = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(50))

class TipoEndereco(Base):
    __tablename__ = "tipo_endereco"
    id_tipo_endereco = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(50))

class TipoImovel(Base):
    __tablename__ = "tipo_imovel"
    id_tipo_imovel = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(50))

class StatusImovel(Base):
    __tablename__ = "status_imovel"
    id_status_imovel = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(50))

class TipoContrato(Base):
    __tablename__ = "tipo_contrato"
    id_tipo_contrato = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(50))

class StatusContrato(Base):
    __tablename__ = "status_contrato"
    id_status_contrato = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(50))

class MetodoPagamento(Base):
    __tablename__ = "metodo_pagamento"
    id_metodo_pagamento = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(50))

class StatusPagamento(Base):
    __tablename__ = "status_pagamento"
    id_status_pagamento = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(50))

class StatusAgendamento(Base):
    __tablename__ = "status_agendamento"
    id_status_agendamento = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(50))

# ===== Entidades Principais =====
class Pessoa(Base):
    __tablename__ = "pessoa"
    id_pessoa = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120))
    cpf_cnpj = Column(String(20), unique=True)
    email = Column(String(120))
    telefone = Column(String(20))
    id_tipo_pessoa = Column(Integer, ForeignKey("tipo_pessoa.id_tipo_pessoa"))
    tipo = relationship("TipoPessoa")
    enderecos = relationship("Endereco", secondary=pessoa_endereco, back_populates="pessoas")

class Endereco(Base):
    __tablename__ = "endereco"
    id_endereco = Column(Integer, primary_key=True, autoincrement=True)
    logradouro = Column(String(120))
    numero = Column(String(10))
    complemento = Column(String(50))
    bairro = Column(String(80))
    cidade = Column(String(80))
    estado = Column(String(2))
    cep = Column(String(15))
    ponto_referencia = Column(String(100))
    pessoas = relationship("Pessoa", secondary=pessoa_endereco, back_populates="enderecos")

class Imovel(Base):
    __tablename__ = "imovel"
    id_imovel = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100))
    descricao = Column(Text)
    id_tipo_imovel = Column(Integer, ForeignKey("tipo_imovel.id_tipo_imovel"))
    id_status_imovel = Column(Integer, ForeignKey("status_imovel.id_status_imovel"))
    valor_venda = Column(Numeric(12, 2))
    valor_aluguel = Column(Numeric(12, 2))
    area_m2 = Column(Numeric(10, 2))
    quartos = Column(Integer)
    banheiros = Column(Integer)
    vagas_garagem = Column(Integer)
    data_cadastro = Column(Date)
    id_proprietario = Column(Integer, ForeignKey("pessoa.id_pessoa"))
    id_endereco = Column(Integer, ForeignKey("endereco.id_endereco"))

    tipo = relationship("TipoImovel")
    status = relationship("StatusImovel")
    proprietario = relationship("Pessoa", foreign_keys=[id_proprietario])
    endereco = relationship("Endereco")
    caracteristicas = relationship("Caracteristica", secondary=imovel_caracteristica)

class Caracteristica(Base):
    __tablename__ = "caracteristica"
    id_caracteristica = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(60))
    descricao = Column(String(255))

class Contrato(Base):
    __tablename__ = "contrato"
    id_contrato = Column(Integer, primary_key=True, autoincrement=True)
    id_tipo_contrato = Column(Integer, ForeignKey("tipo_contrato.id_tipo_contrato"))
    id_status_contrato = Column(Integer, ForeignKey("status_contrato.id_status_contrato"))
    id_imovel = Column(Integer, ForeignKey("imovel.id_imovel"))
    id_cliente = Column(Integer, ForeignKey("pessoa.id_pessoa"))
    id_corretor = Column(Integer, ForeignKey("pessoa.id_pessoa"))
    id_proprietario = Column(Integer, ForeignKey("pessoa.id_pessoa"))
    data_inicio = Column(Date)
    data_fim = Column(Date)
    valor = Column(Numeric(12, 2))
    comissao_percentual = Column(Numeric(5, 2))

class Pagamento(Base):
    __tablename__ = "pagamento"
    id_pagamento = Column(Integer, primary_key=True, autoincrement=True)
    id_contrato = Column(Integer, ForeignKey("contrato.id_contrato"))
    data_pagamento = Column(Date)
    valor_pago = Column(Numeric(12, 2))
    id_metodo_pagamento = Column(Integer, ForeignKey("metodo_pagamento.id_metodo_pagamento"))
    id_status_pagamento = Column(Integer, ForeignKey("status_pagamento.id_status_pagamento"))

class Agendamento(Base):
    __tablename__ = "agendamento"
    id_agendamento = Column(Integer, primary_key=True, autoincrement=True)
    id_imovel = Column(Integer, ForeignKey("imovel.id_imovel"))
    id_cliente = Column(Integer, ForeignKey("pessoa.id_pessoa"))
    id_corretor = Column(Integer, ForeignKey("pessoa.id_pessoa"))
    data_hora = Column(DateTime)
    id_status_agendamento = Column(Integer, ForeignKey("status_agendamento.id_status_agendamento"))
    observacoes = Column(Text)
