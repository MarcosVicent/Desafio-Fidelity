from sqlalchemy.orm import Session
from datetime import datetime
import random
from tqdm import tqdm
from .. import models
from ..utils.web_scraper import WebScraper

class ResultadoPesquisa:
    NADA_CONSTA = 1
    CONSTA_CRIMINAL = 2
    CONSTA_CIVIL = 5
    NAO_ENCONTRADO = 7

class ServicoAutomacao:
    """
    Serviço responsável pela lógica de automação de pesquisas jurídicas.
    Abstrai a interação com o banco de dados e a automação web.
    """

    def __init__(self, db: Session):
        self.db = db

    def executar_pesquisas_lote(self, cod_lote: int):
        """
        Executa a automação de todas as pesquisas de um lote.
        Esta função é chamada assincronamente pela API.
        """

        lote_pesquisas = self.db.query(models.LotePesquisa).filter(
            models.LotePesquisa.cod_lote == cod_lote
        ).all()

        if not lote_pesquisas:
            return

        for lote_pesquisa in tqdm(lote_pesquisas, desc=f"Processando lote {cod_lote}"):
            try:

                pesquisa_detalhe = self.db.query(models.Pesquisa).filter(
                    models.Pesquisa.cod_pesquisa == lote_pesquisa.cod_pesquisa
                ).first()

                if pesquisa_detalhe:
                
                    resultado_web = WebScraper.consultar_tribunal(
                        tipo_documento='cpf',
                        documento=pesquisa_detalhe.cpf
                    )
                    
                    resultado_codificado = self._checar_resultado(resultado_web)
                    
                    self._salvar_resultado(
                        pesquisa_detalhe,
                        lote_pesquisa,
                        resultado_web,
                        resultado_codificado
                    )
                
            except Exception as e:
                
                print(f"Erro ao processar pesquisa {lote_pesquisa.cod_pesquisa}: {e}")
                self._registrar_erro(lote_pesquisa)
                
        self.db.commit()

    def _checar_resultado(self, html_pagina: str) -> int:
        """
        Verifica o conteúdo da página e retorna um código de resultado.
        Método privado para isolar a lógica de verificação.
        """

        if "Não existem informações disponíveis para os parâmetros informados." in html_pagina:
            return ResultadoPesquisa.NADA_CONSTA
        elif ("Processos encontrados" in html_pagina or "Audiências" in html_pagina) and "Criminal" in html_pagina:
            return ResultadoPesquisa.CONSTA_CRIMINAL
        elif ("Processos encontrados" in html_pagina or "Audiências" in html_pagina):
            return ResultadoPesquisa.CONSTA_CIVIL
        else:
            return ResultadoPesquisa.NAO_ENCONTRADO

    def _salvar_resultado(self, pesquisa_detalhe, lote_pesquisa, resultado_web, resultado_codificado):
        """
        Atualiza o banco de dados com os resultados da pesquisa.
        """
        
        pesquisa_detalhe.data_conclusao = datetime.now()
        
        nova_pesquisa_spv = models.PesquisaSPV(
            cod_spv=1,
            cod_spv_computador=36, 
            cod_spv_tipo=pesquisa_detalhe.cod_servico,
            cod_funcionario=-1, 
            filtro=f"CPF: {pesquisa_detalhe.cpf}",
            website_id=1, 
            resultado=str(resultado_codificado)
        )
        self.db.add(nova_pesquisa_spv)
        
        lote_pesquisa.data_conclusao = datetime.now()
        lote_pesquisa.cod_funcionario_conclusao = -1

    def _registrar_erro(self, lote_pesquisa):
        """
        Registra um erro na pesquisa para tratamento posterior.
        """
        
        lote_pesquisa.obs = f"Erro no processamento. Tentativa em {datetime.now()}"