1. Visão Geral da Arquitetura
O sistema é composto por três principais componentes:

Frontend: Uma interface simples em HTML, CSS e JavaScript para o usuário criar e gerenciar lotes de pesquisa. Ele se comunica com a API REST do backend para enviar e receber dados.

Backend: Uma API REST construída com Python e FastAPI. Ele gerencia a lógica de negócio, interage com o banco de dados e orquestra a automação das consultas. O backend é o coração da aplicação.

Banco de Dados: Um banco de dados PostgreSQL que armazena todas as informações do sistema, incluindo dados de pesquisas, lotes, estados e resultados.

A comunicação entre os serviços é feita por meio de requisições HTTP, seguindo o padrão REST. O ambiente de desenvolvimento e produção é isolado e gerenciado por contêineres Docker, garantindo portabilidade e consistência.

2. Tecnologias Utilizadas
Backend:

Python: Linguagem de programação principal.

FastAPI: Framework web de alta performance para a construção da API.

SQLAlchemy: ORM (Object-Relational Mapper) para a abstração da interação com o banco de dados.

Pydantic: Utilizado pelo FastAPI para validação e serialização de dados.

pytest: Framework para a escrita de testes unitários.

Selenium e webdriver-manager: Para a automação de navegadores.

Banco de Dados:

PostgreSQL: Sistema de gerenciamento de banco de dados relacional.

Frontend:

HTML5, CSS3, JavaScript: Para a interface do usuário.

DevOps:

Docker e Docker Compose: Ferramentas para contêinerização e orquestração do ambiente de desenvolvimento.

3. Estrutura de Pastas
A organização do código segue uma abordagem modular e limpa:

.
├── Desafio-Fidelity
├── backend/                  
│   ├── app/                  
│   │   ├── __init__.py
│   │   ├── database.py       
│   │   ├── models.py         
│   │   ├── routes.py         
│   │   └── services/         
│   │   |    └── automacao_servico.py
|   |   |    └── __init__.py
│   │   └── utils/
│   │       └── __init__.py  
|   |       └── web_scraper.py 
│   ├── tests/                
│   │   └── test_routes.py
|   |   └── __init__.py 
│   ├── Dockerfile            
│   ├── requirements.txt      
│   └── main.py               
├── frontend/                 
│   ├── css/                  
│   ├── js/                   
│   └── index.html
├── database_scripts/                 
│    └── 001_criar_tabelas_iniciais                          
├── docker-compose.yml        
└── README.md                 

4. Como Executar o Projeto
Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina.

Clone o Repositório: Se o projeto estivesse em um repositório Git, o primeiro passo seria cloná-lo.

Bash

git clone [url_do_repositorio]
cd [nome_do_projeto]
Construa e Inicie os Contêineres: A partir do diretório raiz do projeto, execute o comando a seguir. Ele irá construir a imagem do backend, baixar a imagem do PostgreSQL e iniciar ambos os serviços.

Bash

docker-compose up --build
A primeira execução pode levar alguns minutos, pois o Docker precisa baixar as imagens e construir o ambiente.

Acesse a Aplicação:

Frontend: Abra o arquivo frontend/index.html diretamente em seu navegador.

API (Backend): Acesse a documentação interativa da API no endereço http://localhost:8000/docs. Você pode testar os endpoints diretamente por lá.

5. Executando Testes Unitários
Para rodar os testes unitários, você pode executar o comando pytest dentro do contêiner do backend.

Acesse o Contêiner do Backend:

Bash

docker-compose exec app /bin/bash
Execute os Testes:

Bash

pytest tests/

6. Scripts de Banco de Dados

O diretório `database_scripts/` contém os scripts SQL para a criação da estrutura inicial do banco de dados.

- `001_criar_tabelas_iniciais.sql`: Contém as instruções `CREATE TABLE` para todas as tabelas do projeto.

Esses scripts são executados automaticamente na primeira inicialização do contêiner PostgreSQL via `docker-compose up`, garantindo que o ambiente do banco de dados seja configurado corretamente.

Licença
Este projeto está licenciado sob a Licença MIT.

Contato
Marcos Vicente - marcosvicente1685@hotmail.com - https://www.linkedin.com/in/marcos-vicente-dos-santos-891283363/

Link do Projeto: https://github.com/MarcosVicent/Desafio-Fidelity

