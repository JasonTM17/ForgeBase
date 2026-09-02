# frozen_string_literal: true

require_relative 'log_severity'

# Minimal leveled logger: ISO-8601 UTC timestamp, severity tag, and service
# context on every line. Errors go to stderr so redirection keeps
# diagnostics out of data pipelines. Replace with a structured logging
# library when the copied-out project needs richer sinks.

module Starter
  class ConsoleLogger
    def initialize(threshold, service)
      @threshold = threshold
      @service = service
    end

    def info(message)
      write(LogSeverity.parse('information'), message)
    end

    def warning(message)
      write(LogSeverity.parse('warning'), message)
    end

    def error(message)
      write(LogSeverity.parse('error'), message)
    end

    private

    def write(severity, message)
      return if severity < @threshold

      line = "#{Time.now.utc.strftime('%Y-%m-%dT%H:%M:%SZ')} " \
             "[#{severity.tag}] service=#{@service} #{message}\n"
      if severity.error?
        warn(line)
      else
        print(line)
      end
    end
  end
end
