# Session 21 Homework — Run TaskBoard with Docker Compose

Ran the class TaskBoard app (`session21-python/`) on my machine: first manually (Vite + Uvicorn + PostgreSQL), then fully containerised with Docker Compose. Tested the frontend, the backend endpoints and every REST API.

Machine: Windows 11, Docker Desktop, PowerShell. All screenshots are from real runs.

---

## Architecture

```text
Browser ──> frontend (nginx, :3000) ──/api──> backend (FastAPI, :8000) ──> postgres (:5432)
              React build                     Alembic migrations on start     named volume postgres-data
```

| Service | Image / build | Port (host → container) | Notes |
|---|---|---|---|
| `frontend` | `./frontend` (Node build → nginx) | 3000 → 80 | nginx serves the React build and proxies `/api` and `/health` to `backend:8000` |
| `backend` | `./backend` (python:3.12-slim) | 8000 → 8000 | runs `alembic upgrade head`, then Uvicorn; non-root user 10001 |
| `postgres` | `postgres:16-alpine` | 5432 → 5432 | data in volume `postgres-data` |

---

## 1. Run manually first

PostgreSQL in Docker, backend and frontend run directly on the machine.

**Backend** — venv, migrations, Uvicorn on port 8080 (the port the Vite dev proxy forwards `/api` to):

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DATABASE_URL = "postgresql+psycopg://taskboard:taskboard@localhost:5432/taskboard"
alembic upgrade head
uvicorn app.main:app --port 8080
```
![alembic migrate](./screenshots/manual-01-backend-migrate.png)
![uvicorn running](./screenshots/manual-04-uvicorn.png)

```powershell
curl.exe -s http://localhost:8080/health
curl.exe -s http://localhost:8080/ready
```
![manual backend test](./screenshots/manual-02-backend-running.png)

**Frontend** — Vite dev server:

```powershell
cd frontend
npm install
npm run dev
```
![vite](./screenshots/manual-05-vite.png)

http://localhost:5173 — shows the task created through the API above:

![manual frontend](./screenshots/manual-03-frontend-vite.png)

---

## 2. Dockerfiles

**Backend — [`backend/Dockerfile`](../backend/Dockerfile)**

```dockerfile
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd --create-home --uid 10001 appuser
COPY alembic.ini ./
COPY alembic ./alembic
COPY app ./app
USER 10001
EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

**Frontend — [`frontend/Dockerfile`](../frontend/Dockerfile)** (multi-stage: build with Node, serve with nginx)

```dockerfile
FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

---

## 3. Docker Compose — [`docker-compose.yml`](../docker-compose.yml)

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: taskboard
      POSTGRES_USER: taskboard
      POSTGRES_PASSWORD: taskboard
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    # backend runs migrations on start, so it must wait until Postgres accepts connections
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U taskboard -d taskboard"]
      interval: 5s
      timeout: 3s
      retries: 10

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql+psycopg://taskboard:taskboard@postgres:5432/taskboard
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    depends_on:
      - backend
    ports:
      - "3000:80"

volumes:
  postgres-data:
```

```powershell
docker compose config --services
docker compose config --quiet
```
![compose config](./screenshots/00-docker-compose-config.png)

### Problem I hit and fixed

With the original file (`depends_on: - postgres`), the backend container **exited with code 1**: `depends_on` only waits for the Postgres container to *start*, not to be *ready*, so `alembic upgrade head` got `Connection refused`.

![backend exited](./screenshots/02-backend-exited-before-fix.png)

Fix: a `pg_isready` healthcheck on `postgres` and `condition: service_healthy` on the backend (plus `restart: unless-stopped`). After that the backend starts cleanly every time.

---

## 4. Run the stack

```powershell
docker compose up -d --build
```
![compose up](./screenshots/01-docker-compose-build.png)

Backend waits for `postgres` to be **Healthy**, then starts.

```powershell
docker compose ps
```
![compose ps](./screenshots/03-docker-compose-ps.png)

All 3 containers up, Postgres healthy.

---

## 5. Backend — http://localhost:8000

**`/docs`** (Swagger UI) — all exposed APIs:

![docs](./screenshots/04-backend-docs.png)

**`/`, `/health`, `/ready`**

```powershell
curl.exe -s http://localhost:8000/
curl.exe -s http://localhost:8000/health
curl.exe -s http://localhost:8000/ready
```
![root health ready](./screenshots/05-backend-root-health.png)
![health browser](./screenshots/05b-backend-health-browser.png)

**`/metrics`** (Prometheus format)

```powershell
curl.exe -s http://localhost:8000/metrics | Select-String '^http_requests_total'
```
![metrics](./screenshots/06-backend-metrics.png)
![metrics browser](./screenshots/06b-backend-metrics-browser.png)

---

## 6. API testing

| Method | Endpoint | Result |
|---|---|---|
| POST | `/api/tasks` | 201, task created |
| GET | `/api/tasks` | list of tasks |
| GET | `/api/tasks/{id}` | one task |
| PUT | `/api/tasks/{id}` | task updated |
| GET | `/api/tasks/stats` | counts by status |
| DELETE | `/api/tasks/{id}` | 204, then GET → 404 |

**POST** — create tasks
![post](./screenshots/07-api-post.png)

**GET** — list all, get one (task 1 was created during the manual run — same DB volume)
![get](./screenshots/08-api-get.png)

**PUT** — move task 3 to DONE, then stats
![put](./screenshots/09-api-put.png)

**DELETE** — create a temp task, delete it, GET returns 404
![delete](./screenshots/10-api-delete.png)

---

## 7. Frontend — http://localhost:3000

Dashboard shows the tasks and counts from the API calls above, so frontend → nginx → backend → Postgres works end to end.

![frontend](./screenshots/11-frontend-running.png)

Through the frontend's nginx proxy:

```powershell
curl.exe -s http://localhost:3000/api/tasks/stats
curl.exe -s http://localhost:3000/health
```
![proxy](./screenshots/12-frontend-api-proxy.png)

---

## 8. Logs

```powershell
docker compose logs backend --tail=12
docker compose logs frontend --tail=4
```
![logs](./screenshots/13-docker-compose-logs.png)

## 9. Backend unit tests

```powershell
cd backend
pytest -v
```
![pytest](./screenshots/14-pytest.png)

`test_create_task_validation` first failed with `no such table: tasks`: the tables are created in a FastAPI startup hook, and `TestClient` only runs startup hooks inside a `with` block. Fixed by calling `startup()` once in `tests/test_api.py`. 3/3 pass.

---

## Result

| Check | Result |
|---|---|
| App runs manually (Vite + Uvicorn + Postgres) | ✅ |
| Backend + frontend Dockerfiles | ✅ |
| `docker compose up -d --build` | ✅ |
| `docker compose ps` — 3 containers up, Postgres healthy | ✅ |
| Frontend http://localhost:3000 | ✅ |
| Backend `/docs`, `/health`, `/ready`, `/metrics` | ✅ |
| GET / POST / PUT / DELETE APIs | ✅ |
| pytest | ✅ 3 passed |

Stop with `docker compose down` (add `-v` to also delete the database volume).
