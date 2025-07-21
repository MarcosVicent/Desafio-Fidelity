CREATE TABLE Estado (
    cod_uf INTEGER PRIMARY KEY,
    uf VARCHAR(2) NOT NULL,
    cod_fornecedor INTEGER,
    nome VARCHAR(255)
);

CREATE TABLE Servico (
    cod_servico INTEGER PRIMARY KEY,
    civil BOOLEAN DEFAULT FALSE,
    criminal BOOLEAN DEFAULT FALSE
);

CREATE TABLE Pesquisa (
    cod_pesquisa SERIAL PRIMARY KEY,
    cod_cliente INTEGER NOT NULL,
    cod_uf INTEGER,
    cod_servico INTEGER,
    tipo VARCHAR(50),
    cpf VARCHAR(14),
    cod_uf_nascimento INTEGER,
    cod_uf_rg INTEGER,
    data_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_conclusao TIMESTAMP,
    nome VARCHAR(255),
    nome_corrigido VARCHAR(255),
    rg VARCHAR(20),
    rg_corrigido VARCHAR(20),
    nascimento DATE,
    mae VARCHAR(255),
    mae_corrigido VARCHAR(255),
    anexo VARCHAR(255),

    FOREIGN KEY (cod_uf) REFERENCES Estado(cod_uf),
    FOREIGN KEY (cod_servico) REFERENCES Servico(cod_servico)
);

CREATE TABLE Lote (
    cod_lote SERIAL PRIMARY KEY,
    cod_lote_prazo INTEGER,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cod_funcionario INTEGER,
    tipo VARCHAR(50),
    prioridade INTEGER
);

CREATE TABLE Lote_Pesquisa (
    cod_lote_pesquisa SERIAL PRIMARY KEY,
    cod_lote INTEGER,
    cod_pesquisa INTEGER,
    cod_funcionario INTEGER,
    cod_funcionario_conclusao INTEGER,
    cod_fornecedor INTEGER,
    data_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_conclusao TIMESTAMP,
    cod_uf INTEGER,
    obs TEXT,

    FOREIGN KEY (cod_lote) REFERENCES Lote(cod_lote),
    FOREIGN KEY (cod_pesquisa) REFERENCES Pesquisa(cod_pesquisa)
);

CREATE TABLE Pesquisa_SPV (
    cod_pesquisa_spv SERIAL PRIMARY KEY,
    cod_spv INTEGER,
    cod_spv_computador INTEGER,
    cod_spv_tipo INTEGER,
    cod_funcionario INTEGER,
    filtro TEXT,
    website_id INTEGER,
    resultado TEXT
);
