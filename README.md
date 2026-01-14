# Desafio MBA Engenharia de Software com IA

Conteúdo gerado por IA e revisado por Anderson de Faria

## 📋 Objetivo do Projeto

Este projeto implementa um sistema de **Perguntas e Respostas (Q&A)** que permite responder perguntas do usuário com base nas informações contidas em um arquivo PDF.

O sistema funciona em três etapas principais:

1. **Ingestão (`ingest.py`)**: Carrega o conteúdo de um PDF, divide o texto em chunks, gera embeddings usando o modelo Google Gemini e armazena os dados vetorizados no PostgreSQL com extensão pgvector.

2. **Busca Semântica (`search.py`)**: Realiza busca semântica no banco de dados vetorial para encontrar os trechos mais relevantes do documento relacionados à pergunta do usuário e gera uma resposta contextualizada usando o modelo Gemini.

3. **Interface de Chat (`chat.py`)**: Fornece uma interface interativa em linha de comando para que o usuário faça perguntas e receba respostas baseadas no conteúdo do PDF.

O projeto já inclui o arquivo `document.pdf` com informações sobre faturamento e ano de fundação de empresas, mas você pode usar qualquer PDF de sua escolha.

---

## 🚀 Passo a Passo para Rodar o Projeto

### Pré-requisitos

- **Python 3.10 ou superior**
- **Docker e Docker Compose** (para rodar o banco de dados PostgreSQL)
- **Conta Google AI** (para obter a chave API do Gemini)

---

### 1. Clone o Repositório

```bash
git clone <url-do-repositorio>
cd mba-ia-desafio-ingestao-busca
```

---

### 2. Criar e Ativar Ambiente Virtual

É altamente recomendado usar um ambiente virtual Python para isolar as dependências do projeto:

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
# No Linux/Mac:
source venv/bin/activate

# No Windows:
# venv\Scripts\activate
```

Após ativar, você verá `(venv)` no início da linha do terminal.

---

### 3. Instalar Dependências

Com o ambiente virtual ativado, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

**Nota**: Se encontrar erros com versões específicas (como `numpy==2.3.2` não encontrado), você pode instalar as dependências principais manualmente:

```bash
pip install langchain-community langchain-text-splitters langchain-core langchain-postgres langchain-google-genai python-dotenv pypdf
```

---

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Chave API do Google AI (Gemini)
# Obtenha em: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=sua_chave_api_aqui

# Caminho relativo para o arquivo PDF (a partir da raiz do projeto)
PDF_PATH=document.pdf

# Modelo de embedding do Google (opcional, padrão: gemini-embedding-001)
GOOGLEAI_MODEL=gemini-embedding-001

# URL de conexão com o banco PostgreSQL
PGVECTOR_URL=postgresql://postgres:postgres@localhost:5432/desafio_ingestao_busca

# Nome da coleção/tabela para armazenar os vetores
PGVECTOR_COLLECTION=documents
```

**Para obter a chave API do Google AI:**
1. Acesse: https://makersuite.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em "Create API Key" ou "Get API Key"
4. Copie a chave gerada e cole no arquivo `.env`

**Importante**: Não compartilhe sua chave API publicamente. O arquivo `.env` já deve estar no `.gitignore`.

---

### 5. Subir o Banco de Dados PostgreSQL

O projeto usa Docker Compose para facilitar a configuração do banco de dados PostgreSQL com a extensão pgvector.

```bash
# Subir o banco de dados em modo detached (background)
docker compose up -d
```

Este comando irá:
- Criar um container PostgreSQL 17 com pgvector
- Criar o banco de dados `desafio_ingestao_busca`
- Configurar usuário e senha (postgres/postgres)
- Expor a porta 5432
- Criar automaticamente a extensão `vector`

**Verificar se o container está rodando:**
```bash
docker ps
```

Você deve ver o container `postgres_desafio_ingestao_busca` na lista.

**Parar o banco de dados:**
```bash
docker compose down
```

**Parar e remover os volumes (apaga os dados):**
```bash
docker compose down -v
```

---

### 6. Executar a Ingestão do PDF

Antes de fazer perguntas, é necessário processar o PDF e carregar os dados no banco de dados vetorial:

```bash
# Com o ambiente virtual ativado
python src/ingest.py
```

Este script irá:
- Carregar o arquivo PDF especificado em `PDF_PATH`
- Dividir o documento em chunks de texto
- Gerar embeddings para cada chunk
- Armazenar os dados no PostgreSQL com pgvector

Aguarde a conclusão da ingestão. Você pode executar este script sempre que quiser atualizar os dados do banco (por exemplo, ao trocar o PDF).

---

### 7. Executar o Chat

Com os dados ingeridos, você pode iniciar o chat interativo:

```bash
# Com o ambiente virtual ativado
python src/chat.py
```

O chat irá iniciar e você poderá fazer perguntas sobre o conteúdo do PDF. Digite `sair` para encerrar.

**Exemplo de uso:**
```
==================================================
Chat iniciado. Digite 'sair' para encerrar.
==================================================
 
Digite sua pergunta: Qual foi o faturamento da empresa X em 2023?
Resposta: [A resposta será gerada baseada no conteúdo do PDF]
```

---

## 🔧 Fluxo Completo do Projeto

```
1. PDF (document.pdf)
   ↓
2. ingest.py → Processa PDF → Gera Embeddings → Armazena no PostgreSQL/pgvector
   ↓
3. Usuário faz pergunta via chat.py
   ↓
4. search.py → Busca semântica no banco → Gera resposta com Gemini → Retorna ao usuário
```

---

## ⚠️ Possíveis Problemas e Soluções

### 1. Erro: `ModuleNotFoundError: No module named 'dotenv'` (ou outras dependências)

**Problema**: Dependências não instaladas ou ambiente virtual não ativado.

**Solução**:
```bash
# Certifique-se de que o ambiente virtual está ativado
source venv/bin/activate

# Reinstale as dependências
pip install -r requirements.txt

# Ou instale os pacotes principais manualmente:
pip install langchain-community langchain-text-splitters langchain-core langchain-postgres langchain-google-genai python-dotenv pypdf
```

---

### 2. Erro: `No matching distribution found for numpy==2.3.2`

**Problema**: Versão específica do numpy não está disponível no PyPI.

**Solução**: Instale as dependências principais manualmente (como mostrado acima) ou atualize o `requirements.txt` para usar uma versão disponível do numpy.

---

### 3. Erro: Container do banco de dados não está rodando

**Problema**: O PostgreSQL não foi iniciado ou o container parou.

**Solução**:
```bash
# Verificar status dos containers
docker ps

# Se o container não estiver listado, suba novamente:
docker compose up -d

# Verificar logs em caso de erro:
docker compose logs postgres
```

---

### 4. Erro: `Connection refused` ou `could not connect to server`

**Problema**: Não é possível conectar ao banco de dados PostgreSQL.

**Soluções**:
- Verifique se o container está rodando: `docker ps`
- Verifique se a porta 5432 está livre: `lsof -i :5432` ou `netstat -an | grep 5432`
- Verifique as credenciais no arquivo `.env` (usuário: postgres, senha: postgres)
- Verifique se a URL de conexão está correta: `postgresql://postgres:postgres@localhost:5432/desafio_ingestao_busca`

---

### 5. Erro: `RuntimeError: Environment variable GOOGLE_API_KEY is not set`

**Problema**: A chave API do Google AI não foi configurada ou o arquivo `.env` não está sendo carregado.

**Soluções**:
- Verifique se o arquivo `.env` existe na raiz do projeto
- Verifique se o arquivo `.env` contém `GOOGLE_API_KEY=sua_chave_aqui`
- Certifique-se de que não há espaços ao redor do `=` no arquivo `.env`
- Verifique se você está executando o script a partir da raiz do projeto

---

### 6. Erro: `Error: Bad status code: 401` ao usar Google AI

**Problema**: Chave API do Google AI inválida ou expirada.

**Solução**:
- Verifique se a chave API está correta no arquivo `.env`
- Gere uma nova chave API em: https://makersuite.google.com/app/apikey
- Certifique-se de que a chave tem permissões adequadas (API do Gemini habilitada)

---

### 7. Erro: `FileNotFoundError` ao executar ingest.py

**Problema**: O arquivo PDF não foi encontrado no caminho especificado.

**Soluções**:
- Verifique se o arquivo PDF existe no caminho especificado em `PDF_PATH` no arquivo `.env`
- O caminho é relativo à raiz do projeto (ex: `document.pdf` para um PDF na raiz)
- Verifique se o nome do arquivo está correto (case-sensitive no Linux)

---

### 8. Erro: `psycopg2.OperationalError: could not connect to server`

**Problema**: Erro de conexão com PostgreSQL (pode ser extensão pgvector não criada).

**Soluções**:
- Verifique se o container está rodando: `docker ps`
- O `docker-compose.yml` já configura a extensão `vector` automaticamente
- Se necessário, recrie os containers: `docker compose down -v && docker compose up -d`

---

### 9. Respostas genéricas ou "Não tenho informações"

**Problema**: A ingestão pode não ter funcionado corretamente ou o PDF não contém a informação.

**Soluções**:
- Verifique se a ingestão foi executada com sucesso (`python src/ingest.py`)
- Verifique se há dados no banco: conecte-se ao PostgreSQL e verifique a tabela/coleção
- Tente fazer perguntas mais específicas sobre o conteúdo do PDF
- Verifique se o PDF foi processado corretamente (alguns PDFs podem ter problemas de encoding)

---

### 10. Ambiente virtual não ativado

**Problema**: Ao executar `python src/ingest.py`, usa o Python do sistema ao invés do ambiente virtual.

**Solução**:
```bash
# Sempre ative o ambiente virtual antes de executar:
source venv/bin/activate

# Ou use o Python do ambiente virtual diretamente:
./venv/bin/python src/ingest.py
```

---

### 11. Erro de permissão ao executar scripts

**Problema**: Scripts Python não têm permissão de execução (Linux/Mac).

**Solução**: Não é necessário dar permissão de execução. Use:
```bash
python src/ingest.py
# ao invés de
./src/ingest.py
```

---

## 📝 Notas Adicionais

- **Trocar o PDF**: Para usar um PDF diferente, atualize a variável `PDF_PATH` no arquivo `.env` e execute `python src/ingest.py` novamente.

- **Limpar e Reingestir**: Se quiser limpar os dados anteriores e reingestir o PDF:
  ```bash
  docker compose down -v
  docker compose up -d
  python src/ingest.py
  ```

- **Customizar Modelo**: Você pode alterar o modelo do Gemini alterando a variável `GOOGLEAI_MODEL` no arquivo `.env` ou modificando diretamente no código (ex: em `search.py`, linha 53).

- **Performance**: A primeira execução pode ser mais lenta devido ao download de modelos e inicialização do banco. Execuções subsequentes serão mais rápidas.

---

## 📚 Estrutura do Projeto

```
mba-ia-desafio-ingestao-busca/
├── src/
│   ├── ingest.py          # Script de ingestão do PDF
│   ├── search.py          # Função de busca semântica e geração de resposta
│   └── chat.py            # Interface interativa de chat
├── docker-compose.yml     # Configuração do PostgreSQL com pgvector
├── requirements.txt       # Dependências Python do projeto
├── document.pdf           # PDF de exemplo com dados
├── .env                   # Variáveis de ambiente (não versionado)
├── .gitignore            # Arquivos ignorados pelo Git
├── README.md             # README original
└── README2.md            # Este arquivo
```

---

## 🆘 Ainda com Problemas?

Se você encontrar problemas não listados aqui:

1. Verifique os logs do Docker: `docker compose logs`
2. Verifique se todas as variáveis de ambiente estão configuradas corretamente
3. Certifique-se de que está usando Python 3.10 ou superior
4. Verifique a documentação do LangChain e Google AI

---

**Boa sorte com o projeto! 🚀**
