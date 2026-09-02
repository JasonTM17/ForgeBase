# frozen_string_literal: true

require "test_helper"

class Api::WidgetsControllerTest < ActionDispatch::IntegrationTest
  test "health trio returns ok" do
    get "/health"
    assert_response :success
    assert_equal({ "status" => "ok" }, response.parsed_body)

    get "/up"
    assert_response :success
  end

  test "creates, fetches, and rejects bad input" do
    post "/api/widgets", params: { widget: { name: "anvil" } }, as: :json
    assert_response :created
    assert_equal "anvil", response.parsed_body.dig("data", "name")

    id = response.parsed_body.dig("data", "id")
    get "/api/widgets/#{id}"
    assert_response :success
    assert_equal "anvil", response.parsed_body.dig("data", "name")

    post "/api/widgets", params: { widget: { name: "  " } }, as: :json
    assert_response :bad_request
    assert_equal "RESOURCE_INVALID", response.parsed_body.dig("error", "code")
  end

  test "missing widget returns not found envelope" do
    get "/api/widgets/999"
    assert_response :not_found
    assert_equal "RESOURCE_NOT_FOUND", response.parsed_body.dig("error", "code")
  end
end
