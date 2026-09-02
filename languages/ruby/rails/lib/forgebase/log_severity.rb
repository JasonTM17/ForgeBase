# frozen_string_literal: true

# Severity levels for the built-in console logger, ordered from most to
# least severe. The declaration order is the severity order.

module Forgebase
  class LogSeverity
    include Comparable

    ORDER = {
      critical: 0,
      error: 1,
      warning: 2,
      information: 3,
      debug: 4,
      trace: 5
    }.freeze

    private_constant :ORDER

    attr_reader :name

    def initialize(name)
      @rank = ORDER.fetch(name.to_sym)
      @name = name.to_s
    end

    def self.parse(value)
      return nil if value.nil?

      symbol = value.to_s.downcase.to_sym
      ORDER.key?(symbol) ? new(symbol) : nil
    end

    def self.names
      ORDER.keys.map(&:to_s)
    end

    def <=>(other)
      @rank <=> other.instance_variable_get(:@rank)
    end

    def tag
      name[0, 3].upcase
    end

    def error?
      @rank <= ORDER[:error]
    end
  end
end
