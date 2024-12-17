# 🚀 To-Do App

**Descrição do projeto:**

Aplicação web para o gerenciamento de tarefas, construída com React (front-end) e Python (back-end).

[Repositório front-end](https://github.com/estefaneluz/to-do-list)

---

## 📋 **Requisitos**

Antes de começar, certifique-se de ter instalado em sua máquina:

- **Python 3.9+**
- **Django**
- **PostgreSQL**
- **Docker e Docker Compose**

---

## 🛠️ **Instalação e Configuração**

### **Clonar o Repositório**

Abra o terminal e execute:

```bash
git clone git@github.com:estefaneluz/to-do-api.git
cd to-do-api
```

### Docker (Recomendável)

1. Crie um arquivo `.env` a partir do `.env-example` e preencha com os dados necessários:

```bash
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=your_secret_key_here
DB_NAME=task_manager_db
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
```

2. Use o comando `docker compose up` para rodar fazer o build e inicializar os containers. A API estará disponível em `http://localhost:8000`.

### Linux

1. Instale as dependências:

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv postgresql postgresql-contrib libpq-dev
```

2. Configure o PostgreSQL

```bash
sudo -u postgres psql
```

```SQL
CREATE DATABASE task_manager_db;
```

3. Instale as dependências do Python

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Rode as migrations e inicie o servidor:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Windows

1. Instale as dependências do Python:

```bash
py -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

2. Instale o PostgreSQL

3. Crie o banco de dados:

```bash
psql -U postgres
```

4. Rode as migrations e inicie o servidor:

```bash
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```