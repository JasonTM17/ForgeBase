# frozen_string_literal: true

# Fail-fast configuration: missing required variables or values that fail
# validation abort startup before any real work happens, so
# misconfiguration is never discovered through request traffic.

module Forgebase
  class Config
    attr_reader :service_name, :log_level

    def initialize(service_name, log_level)
      @service_name = service_name
      @log_level = log_level
    end

    def self.load_from_environment!(environment = ENV)
      service_name = required(environment, 'SERVICE_NAME')
      level_name = optional(environment, 'APP_LOG_LEVEL', 'information')
      log_level = LogSeverity.parse(level_name) ||
                  raise(EnvConfigError,
                        "APP_LOG_LEVEL '#{level_name}' is invalid. Valid values: " \
                        "#{LogSeverity.names.join(', ')}.")
      new(service_name, log_level)
    end

    def self.required(environment, name)
      value = environment[name]
      raise EnvConfigError, "required environment variable #{name} is missing or empty" if
        value.nil? || value.strip.empty?

      value
    end

    def self.optional(environment, name, fallback)
      value = environment[name]
      value.nil? || value.strip.empty? ? fallback : value
    end
  end

  class EnvConfigError < StandardError; end
end
