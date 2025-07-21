import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..app.database import Base, get_db
from ..app.models import Lote, Pesquisa
from ..main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas do banco de dados de teste
Base.metadata.create_all(bind=engine)

# Sobrescreve a dependência do banco de dados na aplicação principal
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_criar_lote():
    """Testa a criação de um novo lote."""
    response = client.post(
        "/lotes/",
        json={"cod_lote_prazo": 7, "cod_funcionario": 1, "tipo": "Novo", "prioridade": 1}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["tipo"] == "Novo"
    assert "cod_lote" in data

def test_criar_pesquisa():
    """Testa a criação de uma nova pesquisa."""
    pesquisa_data = {
        "cod_cliente": 1, "cod_uf": 1, "cod_servico": 1,
        "tipo": "CPF", "cpf": "123.456.789-00", "nome": "João da Silva",
        "nascimento": "1990-01-01", "mae": "Maria da Silva"
    }
    response = client.post("/pesquisas/", json=pesquisa_data)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "João da Silva"

def test_obter_lote_nao_encontrado():
    """Testa a busca de um lote inexistente."""
    response = client.get("/lotes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Lote não encontrado"}
