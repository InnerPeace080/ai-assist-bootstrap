---
name: rust-axum-web
description: Axum 0.7+ web routing, State extractors, type-safe errors with thiserror, and IntoResponse implementation.
author: "Tokio/Axum Community & ai-assist-bootstrap"
version: "1.0.0"
license: "MIT"
metadata:
  origin_repo: "https://github.com/tokio-rs/axum"
  upstream_file: "examples/README.md"
  source_type: "official-grounded"
  lineage: "curated"
  last_upstream_sync: "2026-09-26T23:40:00Z"
  customizations:
    - "Centralized AppError enum with IntoResponse"
    - "sqlx error auto-conversion with thiserror"
    - "Zero unwrap() production rule"
---

# Rust Axum Web Service Runbook

## When to Use
Use this skill when designing HTTP routes, middleware, application state extractors, and error handling in Rust Axum 0.7+ applications.

---

## 1. Centralized Application Error Handling

Never panic or leak database internals to HTTP clients. Implement `IntoResponse` for a custom domain error enum using `thiserror`:

```rust
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("Resource not found: {0}")]
    NotFound(String),

    #[error("Validation failed: {0}")]
    Validation(String),

    #[error("Internal server error")]
    Internal(#[from] anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, client_message) = match self {
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg),
            AppError::Validation(msg) => (StatusCode::BAD_REQUEST, msg),
            AppError::Database(err) => {
                tracing::error!("Database query failed: {:?}", err);
                (StatusCode::INTERNAL_SERVER_ERROR, "Database error occurred".to_string())
            }
            AppError::Internal(err) => {
                tracing::error!("Unexpected internal error: {:?}", err);
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal server error".to_string())
            }
        };

        let body = Json(json!({ "error": client_message }));
        (status, body).into_response()
    }
}
```

---

## 2. Route Handlers & State Extraction

Handlers return `Result<Json<T>, AppError>` using the `?` operator for clean unwinding:

```rust
use axum::{
    extract::{Path, State},
    Json,
};
use std::sync::Arc;

#[derive(Clone)]
pub struct AppState {
    pub db_pool: sqlx::PgPool,
}

pub async fn get_user_by_id(
    State(state): State<Arc<AppState>>,
    Path(user_id): Path<i64>,
) -> Result<Json<UserDto>, AppError> {
    let user = sqlx::query_as!(
        UserDto,
        "SELECT id, email, name FROM users WHERE id = $1",
        user_id
    )
    .fetch_optional(&state.db_pool)
    .await?
    .ok_or_else(|| AppError::NotFound(format!("User {user_id} not found")))?;

    Ok(Json(user))
}
```

---

## 3. Router Composition & Graceful Shutdown

```rust
use axum::{routing::get, Router};
use std::net::SocketAddr;
use tokio::signal;

pub fn create_router(state: Arc<AppState>) -> Router {
    Router::new()
        .route("/users/:id", get(get_user_by_id))
        .with_state(state)
}

pub async fn shutdown_signal() {
    signal::ctrl_c().await.expect("Failed to install CTRL+C handler");
    tracing::info!("Shutdown signal received, draining in-flight requests...");
}
```

---

## 4. Verification Standards
- **Linter**: `cargo clippy --all-targets -- -D warnings`
- **Tests**: `cargo test`

