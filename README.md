# Python — Estudos e Projetos Práticos

Repositório dedicado aos meus estudos e à minha evolução no desenvolvimento com **Python**.

Aqui estão organizados exercícios, desafios e projetos práticos desenvolvidos ao longo da minha jornada de aprendizado, desde os fundamentos da linguagem até o desenvolvimento de APIs, manipulação de bancos de dados e automações.

O objetivo é construir uma base sólida em Python, aplicando os conhecimentos em situações práticas e evoluindo gradualmente para o desenvolvimento de soluções reais.

---

## Tecnologias e ferramentas

- **Python:** linguagem principal de desenvolvimento.
- **SQLite:** banco de dados relacional.
- **Requests:** consumo de APIs e requisições HTTP.
- **FastAPI:** desenvolvimento de APIs.
- **Pydantic:** validação de dados.
- **Pytest:** testes automatizados.
- **HTTPX:** cliente HTTP utilizado nos testes.
- **Git e GitHub:** versionamento e gerenciamento do código.

---

## Conteúdo estudado

### Fundamentos de Python

| Pasta | Conteúdo |
|---|---|
| `dia-01/` | Variáveis, tipos de dados, input, print e condicionais (`if`, `elif`, `else`). |
| `dia-02/` | Estruturas de repetição (`for`, `while`), listas e `range`. |
| `dia-03/` | Dicionários, tuplas e conjuntos (`sets`). |
| `dia-04/` | Funções, parâmetros, `return` e valores padrão. |
| `dia-05/` | Manipulação de arquivos, `open`, `pathlib` e CSV. |
| `dia-06/` | Tratamento de erros (`try/except`) e módulos como `json`, `shutil` e `os`. |

### Semana 04 — Banco de dados e integração com APIs

Pasta: `semana-04/`

- Criação e manipulação de bancos de dados SQLite.
- Consultas SQL (`SELECT`, `WHERE` e agregações).
- Atualização e exclusão de registros.
- Relacionamento entre tabelas com `JOIN`.
- Chaves estrangeiras.
- Desenvolvimento de consultas interativas.
- Integração com APIs de clima.
- Armazenamento de informações em banco de dados.

### Semana 05 — FastAPI e Webhooks

Pasta: `semana-05/`

- Introdução ao FastAPI.
- Criação de endpoints HTTP.
- Desenvolvimento de uma API para recebimento de pedidos.
- Recebimento e processamento de webhooks.
- Validação de dados com Pydantic.
- Organização do projeto em módulos.
- Testes automatizados com Pytest e HTTPX.

**Projeto prático:** API de Webhooks capaz de receber pedidos, validar informações, calcular valores totais e consultar pedidos processados.

---

## Estrutura do repositório

```text
python-conceitos-basicos/
│
├── dia-01/
├── dia-02/
├── dia-03/
├── dia-04/
├── dia-05/
├── dia-06/
│
├── semana-04/
│
├── semana-05/
│   ├── main.py
│   ├── schemas.py
│   ├── services.py
│   ├── test_main.py
│   └── requirements.txt
│
└── README.md
```

---

## Como executar os projetos

### 1. Pré-requisitos

- Python 3.10 ou superior.
- Git.
- Editor de código, como VS Code ou Cursor.

### 2. Clonar o repositório

```bash
git clone URL_DO_SEU_REPOSITORIO
```

Entre na pasta:

```bash
cd python-conceitos-basicos
```

### 3. Criar e ativar o ambiente virtual

Criar:

```bash
python -m venv .venv
```

Ativar no Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

Para os exercícios que utilizam Requests:

```bash
python -m pip install requests
```

Para o projeto da Semana 05:

```bash
python -m pip install -r semana-05/requirements.txt
```

---

## Executando os exercícios

Os exercícios podem ser executados individualmente a partir da raiz do repositório.

Exemplos:

```bash
python dia-01/conceitos.py
python dia-02/fizzbuzz.py
python dia-03/contador_palavras.py
python dia-04/estatisticas_lista.py
python dia-05/agenda_csv.py
python dia-06/agenda_json.py
```

Os demais exercícios estão organizados em suas respectivas pastas.

---

## Executando a API da Semana 05

No PowerShell:

```powershell
cd semana-05
python -m uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

Documentação interativa:

```text
http://127.0.0.1:8000/docs
```

### Executando os testes automatizados

Dentro da pasta `semana-05`, execute:

```bash
python -m pytest -v
```

Os testes verificam o funcionamento dos endpoints, o recebimento de pedidos, a validação de dados e o armazenamento dos pedidos processados.

---

## Objetivos de aprendizado

- Desenvolver lógica de programação.
- Aprimorar conhecimentos em Python.
- Trabalhar com APIs e requisições HTTP.
- Aprender manipulação de bancos de dados.
- Desenvolver integrações entre sistemas.
- Criar automações utilizando Python.
- Aplicar testes automatizados.
- Utilizar boas práticas de organização e versionamento de código.

---

## Status do projeto

**Em desenvolvimento.**

Novos exercícios, projetos e tecnologias serão adicionados conforme a evolução dos estudos.