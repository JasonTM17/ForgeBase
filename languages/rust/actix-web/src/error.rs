//! Centralized error handling: one place maps internal errors to the light
//! JSON envelope contract ({"error": {"code", "message"}}). Production
//! responses never leak stack traces or internal details.

use actix_web::http::StatusCode;
use actix_web::{HttpResponse, ResponseError};
use serde::Serialize;

#[derive(Serialize)]
struct ErrorEnvelope {
    error: ErrorBody,
}

#[derive(Serialize)]
struct ErrorBody {
    code: String,
    message: String,
}

#[derive(Debug)]
pub enum AppError {
    /// 404 — the requested resource does not exist.
    NotFound(String),
    /// 400 — the request payload failed validation.
    Invalid(String),
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            AppError::NotFound(message) => write!(f, "not found: {message}"),
            AppError::Invalid(message) => write!(f, "invalid request: {message}"),
        }
    }
}

impl ResponseError for AppError {
    fn status_code(&self) -> StatusCode {
        match self {
            AppError::NotFound(_) => StatusCode::NOT_FOUND,
            AppError::Invalid(_) => StatusCode::BAD_REQUEST,
        }
    }

    fn error_response(&self) -> HttpResponse {
        let (code, message) = match self {
            AppError::NotFound(message) => ("RESOURCE_NOT_FOUND", message.clone()),
            AppError::Invalid(message) => ("RESOURCE_INVALID", message.clone()),
        };
        HttpResponse::build(self.status_code()).json(ErrorEnvelope {
            error: ErrorBody {
                code: code.to_string(),
                message,
            },
        })
    }
}
