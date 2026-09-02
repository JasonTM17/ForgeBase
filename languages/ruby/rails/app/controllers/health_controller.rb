# frozen_string_literal: true

# Health endpoints for the ForgeBase spec. The Rails-convention /up is
# provided by the framework; /health and its live/ready variants are the
# ForgeBase baseline.

class HealthController < ActionController::Base
  def show
    render json: { status: 'ok' }
  end

  def live
    render json: { status: 'ok' }
  end

  def ready
    render json: { status: 'ok' }
  end
end
