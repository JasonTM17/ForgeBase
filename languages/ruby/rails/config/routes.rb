# frozen_string_literal: true

Rails.application.routes.draw do
  # Reveal health status on /up that returns 200 if the app boots with no exceptions, otherwise 500.
  # Can be used by load balancers and uptime monitors to verify that the app is live.
  get "up" => "rails/health#show", as: :rails_health_check

  # ForgeBase health trio (ecosystem-idiomatic for the ForgeBase spec).
  get '/health', to: 'health#show'
  get '/health/live', to: 'health#live'
  get '/health/ready', to: 'health#ready'

  # Example resource demonstrating the request -> validation -> store -> response flow.
  namespace :api do
    resources :widgets, only: [:index, :show, :create, :destroy]
  end
end
