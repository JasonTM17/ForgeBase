//! API routes: the health trio and the example resource demonstrating the
//! request -> validation -> store -> response flow with envelope errors.
//! The in-memory store is deliberate: Phase-1 templates carry no database.

use std::sync::Mutex;

use actix_web::web::{Data, Json, Path};
use actix_web::{delete, get, post, web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

use crate::error::AppError;

#[derive(Debug, Default)]
pub struct WidgetStore {
    inner: Mutex<Vec<Widget>>,
    next_id: Mutex<u64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Widget {
    pub id: u64,
    pub name: String,
}

#[derive(Debug, Deserialize)]
pub struct CreateWidget {
    pub name: String,
}

pub fn configure(cfg: &mut web::ServiceConfig) {
    cfg.service(health)
        .service(live)
        .service(ready)
        .service(create_widget)
        .service(list_widgets)
        .service(get_widget)
        .service(delete_widget);
}

#[get("/health")]
async fn health() -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "status": "ok" }))
}

#[get("/health/live")]
async fn live() -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "status": "ok" }))
}

#[get("/health/ready")]
async fn ready() -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "status": "ok" }))
}

#[post("/api/widgets")]
async fn create_widget(
    store: Data<WidgetStore>,
    payload: Json<CreateWidget>,
) -> Result<impl Responder, AppError> {
    if payload.name.trim().is_empty() {
        return Err(AppError::Invalid("name is required".to_string()));
    }

    let mut inner = store
        .inner
        .lock()
        .map_err(|_| AppError::Invalid("store poisoned".to_string()))?;
    let mut next_id = store
        .next_id
        .lock()
        .map_err(|_| AppError::Invalid("store poisoned".to_string()))?;
    *next_id += 1;
    let widget = Widget {
        id: *next_id,
        name: payload.name.clone(),
    };
    inner.push(widget.clone());
    Ok(HttpResponse::Created().json(serde_json::json!({
        "data": widget,
        "message": "created"
    })))
}

#[get("/api/widgets")]
async fn list_widgets(store: Data<WidgetStore>) -> Result<impl Responder, AppError> {
    let inner = store
        .inner
        .lock()
        .map_err(|_| AppError::Invalid("store poisoned".to_string()))?;
    Ok(HttpResponse::Ok().json(serde_json::json!({
        "data": inner.clone(),
        "message": "ok"
    })))
}

#[get("/api/widgets/{id}")]
async fn get_widget(store: Data<WidgetStore>, path: Path<u64>) -> Result<impl Responder, AppError> {
    let id = path.into_inner();
    let inner = store
        .inner
        .lock()
        .map_err(|_| AppError::Invalid("store poisoned".to_string()))?;
    inner
        .iter()
        .find(|widget| widget.id == id)
        .cloned()
        .map(|widget| {
            HttpResponse::Ok().json(serde_json::json!({
                "data": widget,
                "message": "ok"
            }))
        })
        .ok_or_else(|| AppError::NotFound(format!("widget {id} not found")))
}

#[delete("/api/widgets/{id}")]
async fn delete_widget(
    store: Data<WidgetStore>,
    path: Path<u64>,
) -> Result<impl Responder, AppError> {
    let id = path.into_inner();
    let mut inner = store
        .inner
        .lock()
        .map_err(|_| AppError::Invalid("store poisoned".to_string()))?;
    let original = inner.len();
    inner.retain(|widget| widget.id != id);
    if inner.len() == original {
        return Err(AppError::NotFound(format!("widget {id} not found")));
    }
    Ok(HttpResponse::NoContent().finish())
}
