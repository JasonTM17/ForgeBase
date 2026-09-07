//! Integration tests through actix's test utilities: health probes, the
//! widget flow, and the envelope error contract.

use actix_starter::api::WidgetStore;
use actix_web::{test, web, App};
use serde_json::Value;

#[actix_web::test]
async fn health_probes_return_ok() {
    let app = test::init_service(
        App::new()
            .app_data(web::Data::new(WidgetStore::default()))
            .configure(actix_starter::api::configure),
    )
    .await;

    for path in ["/health", "/health/live", "/health/ready"] {
        let request = test::TestRequest::get().uri(path).to_request();
        let response = test::call_service(&app, request).await;
        assert!(response.status().is_success(), "{path}");
        let body: Value = test::read_body_json(response).await;
        assert_eq!(body["status"], "ok", "{path}");
    }
}

#[actix_web::test]
async fn widget_flow_creates_and_fetches() {
    let app = test::init_service(
        App::new()
            .app_data(web::Data::new(WidgetStore::default()))
            .configure(actix_starter::api::configure),
    )
    .await;

    let request = test::TestRequest::post()
        .uri("/api/widgets")
        .set_json(serde_json::json!({ "name": "anvil" }))
        .to_request();
    let response = test::call_service(&app, request).await;
    assert!(response.status().is_success());
    let created: Value = test::read_body_json(response).await;
    assert_eq!(created["data"]["name"], "anvil");
    assert_eq!(created["message"], "created");
    let id = created["data"]["id"].as_u64().unwrap();

    let request = test::TestRequest::get()
        .uri(&format!("/api/widgets/{id}"))
        .to_request();
    let response = test::call_service(&app, request).await;
    assert!(response.status().is_success());
    let fetched: Value = test::read_body_json(response).await;
    assert_eq!(fetched["data"]["name"], "anvil");
    assert_eq!(fetched["message"], "ok");
}

#[actix_web::test]
async fn empty_name_is_rejected_with_envelope_error() {
    let app = test::init_service(
        App::new()
            .app_data(web::Data::new(WidgetStore::default()))
            .configure(actix_starter::api::configure),
    )
    .await;

    let request = test::TestRequest::post()
        .uri("/api/widgets")
        .set_json(serde_json::json!({ "name": "  " }))
        .to_request();
    let response = test::call_service(&app, request).await;
    assert_eq!(response.status(), actix_web::http::StatusCode::BAD_REQUEST);
    let body: Value = test::read_body_json(response).await;
    assert_eq!(body["error"]["code"], "RESOURCE_INVALID");
}

#[actix_web::test]
async fn missing_widget_returns_not_found_envelope() {
    let app = test::init_service(
        App::new()
            .app_data(web::Data::new(WidgetStore::default()))
            .configure(actix_starter::api::configure),
    )
    .await;

    let request = test::TestRequest::get()
        .uri("/api/widgets/999")
        .to_request();
    let response = test::call_service(&app, request).await;
    assert_eq!(response.status(), actix_web::http::StatusCode::NOT_FOUND);
    let body: Value = test::read_body_json(response).await;
    assert_eq!(body["error"]["code"], "RESOURCE_NOT_FOUND");
}
