from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebScraper:
    """
    Classe utilitária para a automação de navegadores.
    Utiliza Selenium para interagir com o site do TJSP.
    """

    @staticmethod
    def _configurar_driver():
        """Configura e retorna uma instância do WebDriver com as opções corretas."""
        options = Options()
        options.add_argument("--headless")  
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    @staticmethod
    def consultar_tribunal(tipo_documento: str, documento: str) -> str:
        """
        Acessa o site, preenche o formulário e retorna o HTML da página de resultados.
        Modularizado para suportar diferentes tipos de pesquisa.
        """
        driver = None
        try:
            driver = WebScraper._configurar_driver()
            driver.get("https://esaj.tjsp.jus.br/cpopg/open.do")

            wait = WebDriverWait(driver, 10)

            campo_pesquisa_xpath = "//*[@id='cbPesquisa']"
            wait.until(EC.presence_of_element_located((By.XPATH, campo_pesquisa_xpath)))
            
            if tipo_documento == 'cpf':
                
                tipo_pesquisa = driver.find_element(By.XPATH, campo_pesquisa_xpath)
                tipo_pesquisa.send_keys("Documento da Parte")
                
                campo_input_xpath = "//*[@id='campo_DOCPARTE']"
                wait.until(EC.presence_of_element_located((By.XPATH, campo_input_xpath)))
                campo_input = driver.find_element(By.XPATH, campo_input_xpath)
                campo_input.send_keys(documento)
                
            elif tipo_documento == 'nome':
                
                tipo_pesquisa = driver.find_element(By.XPATH, campo_pesquisa_xpath)
                tipo_pesquisa.send_keys("Nome da Parte")

                campo_input_xpath = "//*[@id='campo_NMPARTE']"
                wait.until(EC.presence_of_element_located((By.XPATH, campo_input_xpath)))
                campo_input = driver.find_element(By.XPATH, campo_input_xpath)
                campo_input.send_keys(documento)
                
            else:
                raise ValueError("Tipo de documento inválido.")

            driver.find_element(By.XPATH, "//*[@id='botaoConsultarProcessos']").click()
            
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            return driver.page_source

        except Exception as e:
            print(f"Erro no web scraper: {e}")
            return "Erro ao consultar o site."
        finally:
            if driver:
                driver.quit()