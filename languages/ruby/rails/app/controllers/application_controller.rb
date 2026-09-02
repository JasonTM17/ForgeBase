# frozen_string_literal: true

# Centralized error handling: one place maps internal errors to the
# framework-idiomatic JSON envelope. Production responses never leak stack
# traces, database errors, internal paths, or secrets.

class ApplicationController < ActionController::Base
  # Only allow modern browsers supporting webp images, web push, badges, import maps, CSS nesting, and CSS :has.
  allow_browser versions: :modern

  rescue_from Forgebase::EnvConfigError, with: :render_error
  rescue_from ActiveRecord::RecordNotFound, with: :render_not_found
  rescue_from StandardError, with: :render_internal

  private

  def render_error(exception)
    render json: envelope('RESOURCE_INVALID', exception.message),
           status: :bad_request
  end

  def render_not_found(exception)
    render json: envelope('RESOURCE_NOT_FOUND', exception.message),
           status: :not_found
  end

  def render_internal(exception)
    message = Rails.env.production? ? 'internal server error' : exception.message
    render json: envelope('INTERNAL_ERROR', message),
           status: :internal_server_error
  end

  def envelope(code, message)
    { error: { code: code, message: message } }
  end
end
