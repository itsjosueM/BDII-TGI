import os, logging
from datetime import date, datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, Pessoa, TipoPessoa, Endereco, TipoImovel, StatusImovel, Imovel, Caracteristica, TipoContrato, StatusContrato, Contrato, MetodoPagamento, StatusPagamento, Pagamento, StatusAgendamento, Agendamento

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@db:5432/imobiliaria')
log.info(f'DATABASE_URL = {DATABASE_URL}')

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

app = FastAPI(title='Imobiliaria - BDII TG')
app.mount('/static', StaticFiles(directory='static'), name='static')

def create_and_seed():
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        try:
            if session.query(TipoPessoa).count() == 0:
                session.add_all([TipoPessoa(id_tipo_pessoa=1, descricao='proprietario'),
                            TipoPessoa(id_tipo_pessoa=2, descricao='corretor'),
                            TipoPessoa(id_tipo_pessoa=3, descricao='cliente')])
            if session.query(Pessoa).count() == 0:
                session.add_all([Pessoa(id_pessoa=1, nome='João Silva', cpf_cnpj='11122233344', email='joao@example.com', telefone='(91)99999-0001', id_tipo_pessoa=1),
                            Pessoa(id_pessoa=2, nome='Ana Corretora', cpf_cnpj='22233344455', email='ana@example.com', telefone='(91)99999-0002', id_tipo_pessoa=2),
                            Pessoa(id_pessoa=3, nome='Carlos Cliente', cpf_cnpj='33344455566', email='carlos@example.com', telefone='(91)99999-0003', id_tipo_pessoa=3)])
            if session.query(Endereco).count() == 0:
                session.add_all([Endereco(id_endereco=1, logradouro='Rua A', numero='10', bairro='Bairro A', cidade='Belém', estado='PA', cep='66000-000'),
                            Endereco(id_endereco=2, logradouro='Av B', numero='200', bairro='Bairro B', cidade='Belém', estado='PA', cep='66000-001'),
                            Endereco(id_endereco=3, logradouro='Trav C', numero='5', bairro='Bairro C', cidade='Belém', estado='PA', cep='66000-002')])
            if session.query(TipoImovel).count() == 0:
                session.add_all([TipoImovel(id_tipo_imovel=1, descricao='Apartamento'), TipoImovel(id_tipo_imovel=2, descricao='Casa'), TipoImovel(id_tipo_imovel=3, descricao='Terreno')])
            if session.query(StatusImovel).count() == 0:
                session.add_all([StatusImovel(id_status_imovel=1, descricao='Disponível'), StatusImovel(id_status_imovel=2, descricao='Vendido'), StatusImovel(id_status_imovel=3, descricao='Alugado')])
            if session.query(Caracteristica).count() == 0:
                session.add_all([Caracteristica(id_caracteristica=1, nome='Piscina', descricao='Piscina privativa'),
                            Caracteristica(id_caracteristica=2, nome='Churrasqueira', descricao='Área gourmet'),
                            Caracteristica(id_caracteristica=3, nome='Garagem', descricao='Vaga coberta')])
            if session.query(TipoContrato).count() == 0:
                session.add_all([TipoContrato(id_tipo_contrato=1, descricao='Venda'), TipoContrato(id_tipo_contrato=2, descricao='Locação'), TipoContrato(id_tipo_contrato=3, descricao='Temporada')])
            if session.query(StatusContrato).count() == 0:
                session.add_all([StatusContrato(id_status_contrato=1, descricao='Ativo'), StatusContrato(id_status_contrato=2, descricao='Concluído'), StatusContrato(id_status_contrato=3, descricao='Cancelado')])
            if session.query(MetodoPagamento).count() == 0:
                session.add_all([MetodoPagamento(id_metodo_pagamento=1, descricao='Boleto'), MetodoPagamento(id_metodo_pagamento=2, descricao='Cartão'), MetodoPagamento(id_metodo_pagamento=3, descricao='Transferência')])
            if session.query(StatusPagamento).count() == 0:
                session.add_all([StatusPagamento(id_status_pagamento=1, descricao='Pendente'), StatusPagamento(id_status_pagamento=2, descricao='Pago'), StatusPagamento(id_status_pagamento=3, descricao='Estornado')])
            if session.query(StatusAgendamento).count() == 0:
                session.add_all([StatusAgendamento(id_status_agendamento=1, descricao='Agendado'), StatusAgendamento(id_status_agendamento=2, descricao='Realizado'), StatusAgendamento(id_status_agendamento=3, descricao='Cancelado')])
            session.commit()
            # imoveis
            if session.query(Imovel).count() == 0:
                session.add_all([Imovel(id_imovel=1, titulo='Apto centro', descricao='Apto 2 quartos', id_tipo_imovel=1, id_status_imovel=1, valor_venda=350000, area_m2=75, quartos=2, banheiros=1, vagas_garagem=1, data_cadastro=date.today(), id_proprietario=1, id_endereco=1),
                            Imovel(id_imovel=2, titulo='Casa Jardim', descricao='Casa 4 quartos', id_tipo_imovel=2, id_status_imovel=1, valor_venda=550000, area_m2=180, quartos=4, banheiros=3, vagas_garagem=2, data_cadastro=date.today(), id_proprietario=1, id_endereco=2),
                            Imovel(id_imovel=3, titulo='Terreno Rural', descricao='Terreno 1000m2', id_tipo_imovel=3, id_status_imovel=1, valor_venda=120000, area_m2=1000, quartos=0, banheiros=0, vagas_garagem=0, data_cadastro=date.today(), id_proprietario=1, id_endereco=3)])
                session.commit()
            # contratos
            if session.query(Contrato).count() == 0:
                session.add_all([Contrato(id_contrato=1, id_tipo_contrato=1, id_status_contrato=2, id_imovel=1, id_cliente=3, id_corretor=2, id_proprietario=1, data_inicio=date(2024,5,10), valor=350000, comissao_percentual=5.0),
                            Contrato(id_contrato=2, id_tipo_contrato=1, id_status_contrato=2, id_imovel=2, id_cliente=3, id_corretor=2, id_proprietario=1, data_inicio=date(2024,8,1), valor=550000, comissao_percentual=4.0),
                            Contrato(id_contrato=3, id_tipo_contrato=2, id_status_contrato=1, id_imovel=3, id_cliente=3, id_corretor=2, id_proprietario=1, data_inicio=date(2025,1,1), data_fim=date(2025,12,31), valor=0, comissao_percentual=0.0)])
                session.commit()
            # pagamentos
            if session.query(Pagamento).count() == 0:
                session.add_all([Pagamento(id_pagamento=1, id_contrato=1, data_pagamento=date(2024,5,12), valor_pago=350000, id_metodo_pagamento=1, id_status_pagamento=2),
                            Pagamento(id_pagamento=2, id_contrato=2, data_pagamento=date(2024,8,5), valor_pago=550000, id_metodo_pagamento=2, id_status_pagamento=2),
                            Pagamento(id_pagamento=3, id_contrato=3, data_pagamento=None, valor_pago=0, id_metodo_pagamento=1, id_status_pagamento=1)])
                session.commit()
            # agendamentos
            if session.query(Agendamento).count() == 0:
                session.add_all([Agendamento(id_agendamento=1, id_imovel=1, id_cliente=3, id_corretor=2, data_hora=datetime(2025,5,20,10,0), id_status_agendamento=2, observacoes='Visita realizada'),
                            Agendamento(id_agendamento=2, id_imovel=2, id_cliente=3, id_corretor=2, data_hora=datetime(2025,6,10,14,0), id_status_agendamento=1, observacoes='Agendado'),
                            Agendamento(id_agendamento=3, id_imovel=3, id_cliente=3, id_corretor=2, data_hora=datetime(2025,7,1,9,0), id_status_agendamento=3, observacoes='Cancelado')])
                session.commit()
        except IntegrityError:
            session.rollback()
            log.info('Dados de exemplo já existem — pulando inserção.')

create_and_seed()

@app.get('/', response_class=HTMLResponse)
def index():
    return HTMLResponse(open('static/index.html','r',encoding='utf-8').read())

@app.get('/imoveis')
def list_imoveis():
    with SessionLocal() as s:
        imoveis = s.query(Imovel).all()
        return [{'id': i.id_imovel, 'titulo': i.titulo, 'valor_venda': float(i.valor_venda or 0), 'proprietario': i.proprietario.nome if i.proprietario else None} for i in imoveis]
@app.get('/media_vendas_por_corretor')
@app.get('/media_vendas_por_corretor')
def media_vendas_por_corretor():
    with SessionLocal() as s:
        rows = s.query(Pessoa.nome, func.avg(Contrato.valor).label('media_venda'))\
            .join(Contrato, Contrato.id_corretor == Pessoa.id_pessoa)\
            .filter(Contrato.id_tipo_contrato == 1)\
            .group_by(Pessoa.nome)\
            .order_by(func.avg(Contrato.valor).desc()).all()
        return [{'corretor': r[0], 'media_venda': float(r[1] or 0)} for r in rows]


@app.get('/top_corretores_vendas')
def top_corretores_vendas():
    with SessionLocal() as s:
        rows = s.query(Pessoa.nome, func.count(Contrato.id_contrato).label('qtd_contratos'),
                    func.sum(Contrato.valor).label('total_vendido'),
                    func.avg(Contrato.valor).label('media_venda'))\
            .join(Contrato, Contrato.id_corretor == Pessoa.id_pessoa)\
            .filter(Contrato.id_tipo_contrato == 1)\
            .group_by(Pessoa.nome)\
            .order_by(func.sum(Contrato.valor).desc())\
            .limit(5).all()
        return [{'corretor': r[0], 'qtd_contratos': int(r[1] or 0),
                    'total_vendido': float(r[2] or 0),
                    'media_venda': float(r[3] or 0)} for r in rows]

'''
@app.get('/consultas/sql_example')
def raw_sql_example():
    with engine.connect() as conn:
        q = text("""
        SELECT p.nome as corretor, COUNT(c.id_contrato) as qtd_contratos, AVG(c.valor) as media_valor
        FROM pessoa p
        JOIN contrato c ON c.id_corretor = p.id_pessoa
        WHERE c.id_tipo_contrato = 1
        GROUP BY p.nome
        ORDER BY qtd_contratos DESC;
        """)
        r = conn.execute(q).fetchall()
        return [dict(row) for row in r]'''
