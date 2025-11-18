# AI Resume Screener

An AI-powered tool to upload, parse, and analyze resumes. This project extracts key information from resumes, stores them in a PostgreSQL database, and provides APIs to match candidates with job descriptions.

---

## 🚀 Features

- Resume upload (PDF)  
- Parse text, extract skills, education, experience  
- Store candidate & resume data in PostgreSQL  
- AI-based resume matching logic  
- REST API built with FastAPI  
- Clean project architecture (routes, models, services, utils)  
- JWT Authentication 

---

## 🛠 Tech Stack

- **FastAPI** (Python backend)  
- **PostgreSQL** (database)  
- **uv** (project/runtime management)  
- **SQLAlchemy**  
- **Pydantic Models**  
- **Docker (optional)**  

---

## 📦 Project Setup

### 🔧 Prerequisites

Make sure the machine has:

- Python 3.13+
- PostgreSQL server installed and running
- `uv` installed
- Git (to clone)

---

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/Govin25/AI_Resume_Screener.git
cd AI_Resume_Screener
```


### ✅ 2. Setup configuration

Create a .env file in the repository root:

```bash
touch .env
```

Add following configurations


```
POSTGRES_USER = postgres
POSTGRES_PASSWORD = password
POSTGRES_DB = db_name
POSTGRES_HOST = localhost
POSTGRES_PORT = 5432
SECRET_KEY = your_secret_key
JWT_ALGORITUM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ACCESS_TOKEN_EXPIRE_DAYS = 7
```


### ✅ 3. Create following tables in postgres

* Go into the bash shell and run the following command


```bash
    psql -U user -d db_name
```

* Execute the tables from **db_schema.txt** file inside the postgres shell.


### ✅ 4. Run the Server

```bash
    uv run fastapi dev
```

