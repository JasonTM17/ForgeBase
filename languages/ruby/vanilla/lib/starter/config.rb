# frozen_string_literal: true

# Fail-fast configuration: missing required variables or values that fail
# validation abort startup before any real work happens, so
# misconfiguration is never discovered in production traffic.

module Starter
  class EnvConfigError < StandardError; end

  EnvConfig = Data.define(:service_name, :log_level)

  module_function

  def load_config(environment = ENV)
    service_name = required(environment, 'SERVICE_NAME')
    level_name = optional(environment, 'APP_LOG_LEVEL', 'information')
    log_level = LogSeverity.parse(level_name) ||
                raise(EnvConfigError,
                      "APP_LOG_LEVEL '#{level_name}' is invalid. Valid values: " \
                      "#{LogSeverity.names.join(', ')}.")
    EnvConfig.new(service_name:, log_level:)
  end

  def required(environment, name)
    value = environment[name]
    raise EnvConfigError, "required environment variable #{name} is missing or empty" if
      value.nil? || value.strip.empty?

    value
  end

  def optional(environment, name, fallback)
    value = environment[name]
    value.nil? || value.strip.empty? ? fallback : value
  end
end
