//! Centralized error handling: one place maps internal errors to the light
//! JSON envelope contract ({"error": {"code", "message"}}). Production
//! responses never leak stack traces or internal details.

use axum::http::StatusCode;
use axum::response::{IntoResponse, Response};
use axum::Json;
use serde::Serialize;

#[derive(Serialize)]
pub struct ErrorEnvelope {
    pub error: ErrorBody,
}

#[derive(Serialize)]
pub struct ErrorBody {
    pub code: String,
    pub message: String,
}

#[derive(Debug)]
pub enum AppError {
    /// 404 — the requested resource does not exist.
    NotFound(String),
    /// 400 — the request payload failed validation.
    Invalid(String),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, code, message) = match self {
            AppError::NotFound(message) => (StatusCode::NOT_FOUND, "RESOURCE_NOT_FOUND", message),
            AppError::Invalid(message) => (StatusCode::BAD_REQUEST, "RESOURCE_INVALID", message),
        };
        let body = ErrorEnvelope {
            error: ErrorBody {
                code: code.to_string(),
                message,
            },
        };
        (status, Json(body)).into_response()
    }
}
