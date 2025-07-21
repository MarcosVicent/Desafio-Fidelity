from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Estado(Base):
    __tablename__ = "estado"
    cod_uf = Column(Integer, primary_key=True)
    uf = Column(String(2))
    cod_fornecedor = Column(Integer)
    nome = Column(String(255))

class Servico(Base):
    __tablename__ = "servico"
    cod_servico = Column(Integer, primary_key=True)
    civil = Column(Boolean)
    criminal = Column(Boolean)

class Pesquisa(Base):
    __tablename__ = "pesquisa"
    cod_pesquisa = Column(Integer, primary_key=True)
    cod_cliente = Column(Integer)
    cod_uf = Column(Integer, ForeignKey("estado.cod_uf"))
    cod_servico = Column(Integer, ForeignKey("servico.cod_servico"))
    tipo = Column(String(50))
    cpf = Column(String(14))
    cod_uf_nascimento = Column(Integer)
    cod_uf_rg = Column(Integer)
    data_entrada = Column(DateTime, default=datetime.now)
    data_conclusao = Column(DateTime, nullable=True)
    nome = Column(String(255))
    nome_corrigido = Column(String(255))
    rg = Column(String(20))
    rg_corrigido = Column(String(20))
    nascimento = Column(Date)
    mae = Column(String(255))
    mae_corrigido = Column(String(255))
    anexo = Column(String(255))
    
    estado_fk = relationship("Estado")
    servico_fk = relationship("Servico")

class Lote(Base):
    __tablename__ = "lote"
    cod_lote = Column(Integer, primary_key=True)
    cod_lote_prazo = Column(Integer)
    data_criacao = Column(DateTime, default=datetime.now)
    cod_funcionario = Column(Integer)
    tipo = Column(String(50))
    prioridade = Column(Integer)

class LotePesquisa(Base):
    __tablename__ = "lote_pesquisa"
    cod_lote_pesquisa = Column(Integer, primary_key=True)
    cod_lote = Column(Integer, ForeignKey("lote.cod_lote"))
    cod_pesquisa = Column(Integer, ForeignKey("pesquisa.cod_pesquisa"))
    cod_funcionario = Column(Integer)
    cod_funcionario_conclusao = Column(Integer, nullable=True)
    cod_fornecedor = Column(Integer)
    data_entrada = Column(DateTime, default=datetime.now)
    data_conclusao = Column(DateTime, nullable=True)
    cod_uf = Column(Integer)
    obs = Column(Text, nullable=True)
    
    lote_fk = relationship("Lote")
    pesquisa_fk = relationship("Pesquisa")

class PesquisaSPV(Base):
    __tablename__ = "pesquisa_spv"
    cod_pesquisa_spv = Column(Integer, primary_key=True)
    cod_spv = Column(Integer)
    cod_spv_computador = Column(Integer)
    cod_spv_tipo = Column(Integer)
    cod_funcionario = Column(Integer)
    filtro = Column(Text)
    website_id = Column(Integer)
    resultado = Column(Text)