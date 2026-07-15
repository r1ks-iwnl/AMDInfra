# AMDInfra

### Backend/Frontend app for hosting & analysis of hardware Functional Coverage reports

## Configuration
Set up .env according to .env.example to avoid unexpected behaviour.

# Command examples

### Backend
From the repository root:

```powershell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
python -m database.seed
```

From the `backend/tests` directory:

```powershell
pytest -v
```

### Database
From the `database` directory:

```powershell
alembic upgrade head
alembic revision --autogenerate -m "your message"
```

### Frontend
From the `frontend` directory:

```powershell
npm install
npm run dev
npm run lint
npm run build
npm run preview
```

## Duplication
Duplicate entries are allowed in the database.

## POST/GET Security
Both methods require logging in.

## Swagger auth
Swagger's client_secret field in the authorization menu is completed behind the scenes given that you have a .env config, and as such you don't need to input anything.