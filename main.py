import os, logging
from datetime import date
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import (
    Base, Pessoa, TipoPessoa, Endereco, TipoImovel, StatusImovel,
    Imovel, Caracteristica, TipoContrato, StatusContrato, Contrato,
    MetodoPagamento, StatusPagamento, Pagamento, StatusAgendamento, Agendamento
)

# ===========================
# ⚙️ Configuração de logs e banco
# ===========================
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@db:5432/imobiliaria')
log.info(f'DATABASE_URL = {DATABASE_URL}')
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

# ===========================
# 🚀 Aplicação FastAPI
# ===========================
app = FastAPI(title='Apache Imobiliária - BDII')
app.mount('/static', StaticFiles(directory='static'), name='static')

# ===========================
# 📦 Criação e carga inicial
# ===========================
def create_and_seed():
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        try:
            # Tipos de Pessoa
            if session.query(TipoPessoa).count() == 0:
                session.add_all([
                    TipoPessoa(id_tipo_pessoa=1, descricao='proprietario'),
                    TipoPessoa(id_tipo_pessoa=2, descricao='corretor'),
                    TipoPessoa(id_tipo_pessoa=3, descricao='cliente')
                ])
            session.commit()

            # Pessoas
            if session.query(Pessoa).count() == 0:
                session.add_all([
                    Pessoa(id_pessoa=1, nome='João Silva', cpf_cnpj='11122233344', email='joao@example.com', telefone='(91)99999-0001', id_tipo_pessoa=1),
                    Pessoa(id_pessoa=2, nome='Ana Corretora', cpf_cnpj='22233344455', email='ana@example.com', telefone='(91)99999-0002', id_tipo_pessoa=2),
                    Pessoa(id_pessoa=3, nome='Carlos Cliente', cpf_cnpj='33344455566', email='carlos@example.com', telefone='(91)99999-0003', id_tipo_pessoa=3),
                    Pessoa(id_pessoa=4, nome='Marcos Vendas', cpf_cnpj='44455566677', email='marcos@example.com', telefone='(91)98888-0004', id_tipo_pessoa=2),
                    Pessoa(id_pessoa=5, nome='Julia Cliente', cpf_cnpj='55566677788', email='julia@example.com', telefone='(91)98777-0005', id_tipo_pessoa=3)
                ])
            session.commit()

            # Endereços
            if session.query(Endereco).count() == 0:
                session.add_all([
                    Endereco(id_endereco=1, logradouro='Rua A', numero='10', bairro='Centro', cidade='Belém', estado='PA', cep='66000-000'),
                    Endereco(id_endereco=2, logradouro='Av B', numero='200', bairro='Batista Campos', cidade='Belém', estado='PA', cep='66000-001'),
                    Endereco(id_endereco=3, logradouro='Trav C', numero='5', bairro='Marco', cidade='Belém', estado='PA', cep='66000-002'),
                    Endereco(id_endereco=4, logradouro='Rua D', numero='88', bairro='Nazaré', cidade='Belém', estado='PA', cep='66000-003')
                ])
            session.commit()

            # Tipo e Status de Imóvel
            if session.query(TipoImovel).count() == 0:
                session.add_all([
                    TipoImovel(id_tipo_imovel=1, descricao='Apartamento'),
                    TipoImovel(id_tipo_imovel=2, descricao='Casa'),
                    TipoImovel(id_tipo_imovel=3, descricao='Terreno'),
                    TipoImovel(id_tipo_imovel=4, descricao='Cobertura')
                ])
            session.commit()

            if session.query(StatusImovel).count() == 0:
                session.add_all([
                    StatusImovel(id_status_imovel=1, descricao='Disponível'),
                    StatusImovel(id_status_imovel=2, descricao='Vendido'),
                    StatusImovel(id_status_imovel=3, descricao='Alugado')
                ])
            session.commit()

            # Características
            if session.query(Caracteristica).count() == 0:
                session.add_all([
                    Caracteristica(id_caracteristica=1, nome='Piscina', descricao='Piscina privativa'),
                    Caracteristica(id_caracteristica=2, nome='Garagem', descricao='2 vagas cobertas'),
                    Caracteristica(id_caracteristica=3, nome='Jardim', descricao='Área verde ampla')
                ])
            session.commit()

            # Tipos e Status de Contrato
            if session.query(TipoContrato).count() == 0:
                session.add_all([
                    TipoContrato(id_tipo_contrato=1, descricao='Venda'),
                    TipoContrato(id_tipo_contrato=2, descricao='Locação')
                ])
            session.commit()

            if session.query(StatusContrato).count() == 0:
                session.add_all([
                    StatusContrato(id_status_contrato=1, descricao='Ativo'),
                    StatusContrato(id_status_contrato=2, descricao='Concluído'),
                    StatusContrato(id_status_contrato=3, descricao='Cancelado')
                ])
            session.commit()

            # Imóveis
            if session.query(Imovel).count() == 0:
                session.add_all([
                    Imovel(titulo='Apto centro', descricao='Apto 2 quartos', id_tipo_imovel=1, id_status_imovel=1, valor_venda=350000, area_m2=75, quartos=2, banheiros=1, vagas_garagem=1, data_cadastro=date.today(), id_proprietario=1, id_endereco=1),
                    Imovel(titulo='Casa Jardim', descricao='Casa 4 quartos', id_tipo_imovel=2, id_status_imovel=1, valor_venda=550000, area_m2=180, quartos=4, banheiros=3, vagas_garagem=2, data_cadastro=date.today(), id_proprietario=1, id_endereco=2),
                    Imovel(titulo='Terreno Rural', descricao='Terreno 1000m²', id_tipo_imovel=3, id_status_imovel=1, valor_venda=120000, area_m2=1000, quartos=0, banheiros=0, vagas_garagem=0, data_cadastro=date.today(), id_proprietario=1, id_endereco=3),
                    Imovel(titulo='Cobertura Vista Rio', descricao='Cobertura de luxo', id_tipo_imovel=4, id_status_imovel=1, valor_venda=850000, area_m2=220, quartos=3, banheiros=3, vagas_garagem=2, data_cadastro=date.today(), id_proprietario=1, id_endereco=4)
                ])
            session.commit()

            # Contratos
            if session.query(Contrato).count() == 0:
                session.add_all([
                    Contrato(id_tipo_contrato=1, id_status_contrato=2, id_imovel=1, id_cliente=3, id_corretor=2, id_proprietario=1, data_inicio=date(2024,5,10), valor=350000, comissao_percentual=5.0),
                    Contrato(id_tipo_contrato=1, id_status_contrato=2, id_imovel=2, id_cliente=5, id_corretor=4, id_proprietario=1, data_inicio=date(2024,8,1), valor=550000, comissao_percentual=4.0),
                    Contrato(id_tipo_contrato=2, id_status_contrato=1, id_imovel=3, id_cliente=3, id_corretor=2, id_proprietario=1, data_inicio=date(2025,1,1), valor=0, comissao_percentual=0.0)
                ])
            session.commit()

            # Métodos e Status de Pagamento
            if session.query(MetodoPagamento).count() == 0:
                session.add_all([
                    MetodoPagamento(id_metodo_pagamento=1, descricao='Boleto'),
                    MetodoPagamento(id_metodo_pagamento=2, descricao='Cartão'),
                    MetodoPagamento(id_metodo_pagamento=3, descricao='Transferência')
                ])
            session.commit()

            if session.query(StatusPagamento).count() == 0:
                session.add_all([
                    StatusPagamento(id_status_pagamento=1, descricao='Pendente'),
                    StatusPagamento(id_status_pagamento=2, descricao='Pago'),
                    StatusPagamento(id_status_pagamento=3, descricao='Estornado')
                ])
            session.commit()

            # Agendamentos
            if session.query(StatusAgendamento).count() == 0:
                session.add_all([
                    StatusAgendamento(id_status_agendamento=1, descricao='Agendado'),
                    StatusAgendamento(id_status_agendamento=2, descricao='Realizado'),
                    StatusAgendamento(id_status_agendamento=3, descricao='Cancelado')
                ])
            session.commit()

        except IntegrityError:
            session.rollback()
            log.info('⚠️ Dados já existentes, pulando inserção.')

create_and_seed()

# ===========================
# 🌐 Rotas principais
# ===========================

@app.get('/', response_class=HTMLResponse)
def index():
    return HTMLResponse(open('static/index.html', 'r', encoding='utf-8').read())

@app.get('/imoveis')
def listar_imoveis():
    with SessionLocal() as s:
        imoveis = s.query(Imovel).all()
        return [
            {
                'id': i.id_imovel,
                'titulo': i.titulo,
                'valor_venda': float(i.valor_venda or 0),
                'proprietario': i.proprietario.nome if i.proprietario else None
            } for i in imoveis
        ]

@app.post('/imoveis')
def criar_imovel(data: dict):
    with SessionLocal() as s:
        try:
            novo = Imovel(
                titulo=data.get('titulo'),
                descricao=data.get('descricao'),
                valor_venda=data.get('valor_venda'),
                id_tipo_imovel=1,
                id_status_imovel=1,
                area_m2=100,
                quartos=2,
                banheiros=1,
                vagas_garagem=1,
                data_cadastro=date.today(),
                id_proprietario=data.get('id_proprietario'),
                id_endereco=1
            )
            s.add(novo)
            s.commit()
            return {"mensagem": "Imóvel criado com sucesso!"}
        except Exception as e:
            s.rollback()
            raise HTTPException(status_code=400, detail=str(e))

@app.put('/imoveis/{id_imovel}')
def atualizar_imovel(id_imovel: int, data: dict):
    with SessionLocal() as s:
        imovel = s.get(Imovel, id_imovel)
        if not imovel:
            raise HTTPException(status_code=404, detail="Imóvel não encontrado.")
        try:
            if 'titulo' in data:
                imovel.titulo = data['titulo']
            if 'valor_venda' in data:
                imovel.valor_venda = data['valor_venda']
            s.commit()
            return {"mensagem": "Imóvel atualizado com sucesso!"}
        except Exception as e:
            s.rollback()
            raise HTTPException(status_code=400, detail=str(e))

@app.put('/imoveis/{id_imovel}/arquivar')
def arquivar_imovel(id_imovel: int):
    with SessionLocal() as s:
        imovel = s.get(Imovel, id_imovel)
        if not imovel:
            raise HTTPException(status_code=404, detail="Imóvel não encontrado.")

        try:
            # Tenta encontrar o status 'Arquivado'
            status_arquivado = s.query(StatusImovel).filter_by(descricao='Arquivado').first()

            # Se não existir, cria automaticamente (sem definir ID manual)
            if not status_arquivado:
                status_arquivado = StatusImovel(descricao='Arquivado')
                s.add(status_arquivado)
                s.commit()
                s.refresh(status_arquivado)

            # Atualiza o status do imóvel
            imovel.id_status_imovel = status_arquivado.id_status_imovel
            s.commit()

            return {"mensagem": f"🏷️ Imóvel '{imovel.titulo}' foi arquivado com sucesso!"}

        except Exception as e:
            s.rollback()
            raise HTTPException(status_code=400, detail=f"Erro ao arquivar imóvel: {e}")


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
        rows = s.query(
            Pessoa.nome,
            func.count(Contrato.id_contrato).label('qtd_contratos'),
            func.sum(Contrato.valor).label('total_vendido'),
            func.avg(Contrato.valor).label('media_venda')
        ).join(Contrato, Contrato.id_corretor == Pessoa.id_pessoa)\
        .filter(Contrato.id_tipo_contrato == 1)\
        .group_by(Pessoa.nome)\
        .order_by(func.sum(Contrato.valor).desc())\
        .limit(5).all()
        return [
            {
                'corretor': r[0],
                'qtd_contratos': int(r[1] or 0),
                'total_vendido': float(r[2] or 0),
                'media_venda': float(r[3] or 0)
            } for r in rows
        ]
