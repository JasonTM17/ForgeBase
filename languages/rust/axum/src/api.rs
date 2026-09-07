//! API routes: the health trio and the example resource demonstrating the
//! request -> validation -> store -> response flow with envelope errors.
//! The in-memory store is deliberate: Phase-1 templates carry no database.

use std::collections::HashMap;
use std::sync::{Arc, Mutex};

use axum::extract::{Path, State};
use axum::http::StatusCode;
use axum::routing::{delete, get, post};
use axum::{Json, Router};
use serde::{Deserialize, Serialize};

use crate::error::AppError;

#[derive(Clone, Copy)]
pub struct AppState;

type WidgetStore = Arc<Mutex<HashMap<u64, Widget>>>;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Widget {
    pub id: u64,
    pub name: String,
}

#[derive(Debug, Deserialize)]
pub struct CreateWidget {
    pub name: String,
}

async fn health() -> Json<serde_json::Value> {
    Json(serde_json::json!({ "status": "ok" }))
}

pub fn router(state: AppState) -> Router {
    let widgets: WidgetStore = Arc::new(Mutex::new(HashMap::new()));
    Router::new()
        .route("/health", get(health))
        .route("/health/live", get(health))
        .route("/health/ready", get(health))
        .route("/api/widgets", post(create_widget).get(list_widgets))
        .route("/api/widgets/{id}", get(get_widget))
        .route("/api/widgets/{id}", delete(delete_widget))
        .with_state((state, widgets))
}

async fn create_widget(
    State((_, widgets)): State<(AppState, WidgetStore)>,
    Json(payload): Json<CreateWidget>,
) -> Result<(StatusCode, Json<serde_json::Value>), AppError> {
    if payload.name.trim().is_empty() {
        return Err(AppError::Invalid("name is required".to_string()));
    }

    let mut store = widgets
        .lock()
        .map_err(|_| AppError::Invalid("store poisoned".to_string()))?;
    let id = store.keys().copied().max().unwrap_or(0) + 1;
    let widget = Widget {
        id,
        name: payload.name,
    };
    store.insert(id, widget.clone());
    Ok((
        StatusCode::CREATED,
        Json(serde_json::json!({ "data": widget, "message": "created" })),
    ))
}

async fn list_widgets(
    State((_, widgets)): State<(AppState, WidgetStore)>,
) -> Result<Json<serde_json::Value>, AppError> {
    let store = widgets
        .lock()
        .map_err(|_| AppError::Invalid("store poisoned".to_string()))?;
    let mut all: Vec<Widget> = store.values().cloned().collect();
    all.sort_by_key(|widget| widget.id);
    Ok(Json(serde_json::json!({ "data": all, "message": "ok" })))
}

async fn get_widget(
    State((_, widgets)): State<(AppState, WidgetStore)>,
    Path(id): Path<u64>,
) -> Result<Json<serde_json::Value>, AppError> {
    let store = widgets
        .lock()
        .map_err(|_| AppError::Invalid("store poisoned".to_string()))?;
    store
        .get(&id)
        .cloned()
        .map(|widget| Json(serde_json::json!({ "data": widget, "message": "ok" })))
        .ok_or_else(|| AppError::NotFound(format!("widget {id} not found")))
}

async fn delete_widget(
    State((_, widgets)): State<(AppState, WidgetStore)>,
    Path(id): Path<u64>,
) -> Result<StatusCode, AppError> {
    let mut store = widgets
        .lock()
        .map_err(|_| AppError::Invalid("store poisoned".to_string()))?;
    store
        .remove(&id)
        .map(|_| StatusCode::NO_CONTENT)
        .ok_or_else(|| AppError::NotFound(format!("widget {id} not found")))
}
