from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..app import models
from ..app.database import get_db
from ..app.services.automacao_servico import ServicoAutomacao

router = APIRouter()

@router.post("/lotes/", status_code=status.HTTP_201_CREATED)
def criar_lote(lote: dict, db: Session = Depends(get_db)):
    """Cria um novo lote de pesquisas."""

    novo_lote = models.Lote(**lote)
    db.add(novo_lote)
    db.commit()
    db.refresh(novo_lote)
    return novo_lote

@router.post("/pesquisas/", status_code=status.HTTP_201_CREATED)
def criar_pesquisa(pesquisa: dict, db: Session = Depends(get_db)):
    """Cria uma nova pesquisa."""

    nova_pesquisa = models.Pesquisa(**pesquisa)
    db.add(nova_pesquisa)
    db.commit()
    db.refresh(nova_pesquisa)
    return nova_pesquisa

@router.post("/lotes/{cod_lote}/processar")
def processar_lote(cod_lote: int, db: Session = Depends(get_db)):
    """Processa um lote de pesquisas."""

    lote = db.query(models.Lote).filter(models.Lote.cod_lote == cod_lote).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote não encontrado")
    
    servico = ServicoAutomacao(db)
    servico.executar_pesquisas_lote(cod_lote)
    return {"message": f"Lote {cod_lote} processado com sucesso."}

@router.get("/lotes/{cod_lote}", response_model=dict)
def obter_lote(cod_lote: int, db: Session = Depends(get_db)):
    """Retorna os detalhes de um lote e suas pesquisas."""
    
    lote = db.query(models.Lote).filter(models.Lote.cod_lote == cod_lote).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote não encontrado")
    
    pesquisas_do_lote = db.query(models.LotePesquisa).filter(models.LotePesquisa.cod_lote == cod_lote).all()
    return {
        "lote": lote,
        "pesquisas": pesquisas_do_lote
    }