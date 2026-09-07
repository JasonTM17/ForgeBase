//! Integration tests through the public router: health probes, the widget
//! flow, and the envelope error contract.

use axum::body::Body;
use axum::http::{Request, StatusCode};
use axum_starter::api::{router, AppState};
use http_body_util::BodyExt;
use serde_json::Value;
use tower::ServiceExt;

async fn send(app: axum::Router, request: Request<Body>) -> (StatusCode, Value) {
    let response = app.oneshot(request).await.unwrap();
    let status = response.status();
    let body = response.into_body().collect().await.unwrap().to_bytes();
    let json = if body.is_empty() {
        Value::Null
    } else {
        serde_json::from_slice(&body).unwrap()
    };
    (status, json)
}

#[tokio::test]
async fn health_probes_return_ok() {
    let app = router(AppState);
    for path in ["/health", "/health/live", "/health/ready"] {
        let (status, body) =
            send(app.clone(), Request::get(path).body(Body::empty()).unwrap()).await;
        assert_eq!(status, StatusCode::OK, "{path}");
        assert_eq!(body["status"], "ok", "{path}");
    }
}

#[tokio::test]
async fn widget_flow_validates_creates_and_rejects_bad_input() {
    let app = router(AppState);

    let (status, created) = send(
        app.clone(),
        Request::post("/api/widgets")
            .header("content-type", "application/json")
            .body(Body::from(r#"{ "name": "anvil" }"#))
            .unwrap(),
    )
    .await;
    assert_eq!(status, StatusCode::CREATED);
    assert_eq!(created["data"]["name"], "anvil");
    assert_eq!(created["message"], "created");
    let id = created["data"]["id"].as_u64().unwrap();

    let (status, fetched) = send(
        app.clone(),
        Request::get(format!("/api/widgets/{id}"))
            .body(Body::empty())
            .unwrap(),
    )
    .await;
    assert_eq!(status, StatusCode::OK);
    assert_eq!(fetched["data"]["name"], "anvil");
    assert_eq!(fetched["message"], "ok");
}

#[tokio::test]
async fn empty_name_is_rejected_with_envelope_error() {
    let app = router(AppState);
    let (status, body) = send(
        app,
        Request::post("/api/widgets")
            .header("content-type", "application/json")
            .body(Body::from(r#"{ "name": "  " }"#))
            .unwrap(),
    )
    .await;
    assert_eq!(status, StatusCode::BAD_REQUEST);
    assert_eq!(body["error"]["code"], "RESOURCE_INVALID");
}

#[tokio::test]
async fn missing_widget_returns_not_found_envelope() {
    let app = router(AppState);
    let (status, body) = send(
        app,
        Request::get("/api/widgets/999")
            .body(Body::empty())
            .unwrap(),
    )
    .await;
    assert_eq!(status, StatusCode::NOT_FOUND);
    assert_eq!(body["error"]["code"], "RESOURCE_NOT_FOUND");
}
