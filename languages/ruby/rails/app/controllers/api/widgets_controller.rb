# frozen_string_literal: true

# Example resource demonstrating the request -> validation -> store ->
# response flow with envelope errors. Replace it when copying the template
# out.

class Api::WidgetsController < ApplicationController
  def index
    render json: { data: Widget.all, message: 'ok' }
  end

  def show
    widget = Widget.find(params[:id].to_i)
    if widget
      render json: { data: widget, message: 'ok' }
    else
      render json: envelope('RESOURCE_NOT_FOUND', "widget #{params[:id]} not found"),
             status: :not_found
    end
  end

  def create
    name = params.dig(:widget, :name) || params[:name]
    if name.blank?
      return render json: envelope('RESOURCE_INVALID', 'name is required'),
                    status: :bad_request
    end

    render json: { data: Widget.create(name), message: 'ok' }, status: :created
  end

  def destroy
    if Widget.delete(params[:id].to_i)
      head :no_content
    else
      render json: envelope('RESOURCE_NOT_FOUND', "widget #{params[:id]} not found"),
             status: :not_found
    end
  end
end
