```markdown
# Personal Blog - FastAPI Backend

This repository contains a FastAPI backend for a personal blog application.

Features implemented:
- MySQL (configurable via DB_URL)
- JWT authentication (login/register)
- Phone-based password recovery via OTP (development mode prints/returns OTP)
- Account deletion (注销) and logout (token blacklist)
- Profile management (个人资料) including avatar upload
- Blog CRUD: create, read, update, delete
- Follow/unfollow users
- Private messages (存储为消息记录)，plus a WebSocket endpoint for real-time messages
- File uploads (avatars and blog covers) saved to ./uploads and served as static files

Notes:
- Frontend will be implemented later (Vue + React). For now this backend exposes REST + WebSocket APIs.
- For local testing you can run MySQL via Docker (example below) or point DB_URL to an existing MySQL instance.

Local MySQL (Docker) quick start:
```bash
docker run --name local-mysql -e MYSQL_ROOT_PASSWORD=rootpass -e MYSQL_DATABASE=blogdb -e MYSQL_USER=bloguser -e MYSQL_PASSWORD=blogpass -p 3306:3306 -d mysql:8
```

Environment:
- Copy `.env.example` to `.env` and modify values as needed.

Run (development):
```bash
python -m pip install -r requirements.txt
cp .env.example .env
# adjust DB_URL if needed
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Database migration:
- This template uses SQLAlchemy ORM without Alembic to keep things simple.
- On first run, the application will create tables automatically.

Testing:
- Use the included `test_main.http` file or interact via Swagger at `http://127.0.0.1:8000/docs`.

Project layout:
- app/
  - main.py
  - core/config.py
  - db/session.py
  - models.py
  - schemas.py
  - crud.py
  - api/routers/*.py
  - api/deps.py
  - utils/security.py
  - utils/storage.py
- uploads/ (created automatically)

If you want me to:
- add Alembic migrations,
- integrate real SMS provider for OTP,
- add Dockerfile / docker-compose for the full stack,
please tell me and I will prepare the next steps.
```