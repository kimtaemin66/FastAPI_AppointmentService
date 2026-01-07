**- 서비스 데이터베이스 설계도**
![Image_20251218_174021_693](https://github.com/user-attachments/assets/2bbcea2d-ccee-4a78-bbf7-06679c2a9a7f)

**- Fastapi 설치**
```python
pip install "fastapi[all]"
```

**- Poetry 설치**
```python
pip install poetry
```

**- Poetry : pyproject.toml 생성**
```python
[project]
name = "fastapi-meeting-service"
version = "0.1.0"
description = "edit fastapi test code"
authors = [
    {name = "tmk5415",email = "tmk5415@withrobot.com"}
]
readme = "README.md"
requires-python = "^3.12"
dependencies = [
]

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

**- 필요 패키지 설치하기**
```
poetry add sqlmodel sqlalchemy-utc aiosqlite alembic greenlet "pwdlib[argon2,bcrypt]"
```

**- alembic 초기화**
```
alembic init alembic
```
**- alembic으로 마이그레이션 실행**
```
alembic revision -m "Initialization"
```
**- alembic으로 자동 마이그레이션 실행**
```
alembic revision --autogenerate -m "Auto generate migration"
```
**- FastAPI 실행하기**
```python
fastapi dev app.py
```

sa.Column('file', fastapi_storages.integrations.sqlalchemy.FileType(storage=FileSystemStorage(path="uploads/bookings")), nullable=False),
