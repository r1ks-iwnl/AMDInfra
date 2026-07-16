# AMDInfra

### Backend/Frontend app for hosting & analysis of hardware Functional Coverage reports

## Requirements
**Python (v3.11 or higher)** — [Download Python](https://www.python.org/downloads/)

**Node.js (v18.x or higher)** — [Download Node.js](https://nodejs.org/)

## Configuration
Set up .env according to .env.example to avoid unexpected behaviour.

# Setup commands

### Backend
From the repository root:

Set up python virtual environment:
```powershell
python -m venv .venv
```

In bash activate virtual environment:
```bash
source ./.venv/Scripts/activate
```

Install required libraries:
```powershell
pip install -r requirements.txt
```

From the `database` directory generate the database tables:

```powershell
alembic upgrade head
```

Back in `root` seed database with logs provided by `logs/`:
```powershell
python -m database.seed
```

Run server at `http://localhost:8000`:
```powershell
uvicorn backend.app.main:app
```


You may also run tests from the `backend/tests` directory:

```powershell
pytest -v
```

### Frontend
From the `frontend` directory:

Install libraries and run the server at `http://localhost:5173`:
```powershell
npm install
npm run dev
```

## Duplication
Duplicate entries are allowed in the database.

## POST/GET Security
Both methods require logging in.

## Swagger auth
Swagger's client_secret field in the authorization menu is completed behind the scenes given that you have a .env config, and as such you don't need to input anything.