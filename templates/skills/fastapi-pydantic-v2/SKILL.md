---
name: fastapi-pydantic-v2
description: FastAPI application structure, Pydantic v2 validators, async SQLAlchemy 2.0 sessions, and dependency injection.
author: "FastAPI Community & ai-assist-bootstrap"
version: "1.0.0"
license: "MIT"
metadata:
  origin_repo: "https://github.com/tiangolo/full-stack-fastapi-template"
  upstream_file: "backend/README.md"
  source_type: "official-grounded"
  lineage: "curated"
  last_upstream_sync: "2026-09-26T23:40:00Z"
  customizations:
    - "Pydantic v2 field_validator and model_validator syntax"
    - "SQLAlchemy 2.0 async_sessionmaker generator pattern"
    - "expire_on_commit=False safety rule"
---

# FastAPI & Pydantic v2 Runbook

## When to Use
Use this skill when designing FastAPI endpoints, validating request/response bodies with Pydantic v2, managing async SQLAlchemy 2.0 database sessions, or configuring routers.

---

## 1. Pydantic v2 Validation Standards

- Never use deprecated Pydantic v1 methods (`@validator`, `@root_validator`).
- Use `@field_validator` for single-field transformations and validation.
- Use `@model_validator(mode="after")` for cross-field consistency checks.

```python
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing_extensions import Self

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)
    confirm_password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v.lower()

    @model_validator(mode="after")
    def verify_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
```

---

## 2. Async SQLAlchemy 2.0 Session Dependency

Manage sessions safely using generator dependency injection:

```python
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/app"

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, # Critical for async attribute access after commit
    autoflush=False,
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

---

## 3. Router & Handler Separation

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db_session),
) -> UserResponse:
    # Use services or queries cleanly
    user = await user_service.create(db, payload)
    return user
```

---

## 4. Verification & Linting
- **Linting & Formatting**: `uv run ruff check .` and `uv run ruff format .`
- **Type Checking**: `uv run mypy .`
- **Testing**: `uv run pytest -v`

