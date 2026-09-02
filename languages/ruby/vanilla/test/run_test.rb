# frozen_string_literal: true

$LOAD_PATH.unshift File.expand_path('../lib', __dir__)
require 'minitest/autorun'
require 'starter'

module StarterTests
  class EnvConfigTest < Minitest::Test
    def test_raises_when_required_variable_is_missing
      error = assert_raises(Starter::EnvConfigError) do
        Starter.load_config({})
      end
      assert_includes error.message, 'SERVICE_NAME'
    end

    def test_raises_when_required_variable_is_empty
      assert_raises(Starter::EnvConfigError) do
        Starter.load_config({ 'SERVICE_NAME' => '  ' })
      end
    end

    def test_defaults_log_level_to_information
      config = Starter.load_config({ 'SERVICE_NAME' => 'demo' })
      assert_equal 'information', config.log_level.name
    end

    def test_raises_on_unknown_log_level
      assert_raises(Starter::EnvConfigError) do
        Starter.load_config({ 'SERVICE_NAME' => 'demo', 'APP_LOG_LEVEL' => 'loud' })
      end
    end

    def test_parses_log_level_case_insensitively
      config = Starter.load_config(
        { 'SERVICE_NAME' => 'demo', 'APP_LOG_LEVEL' => 'Warning' }
      )
      assert_equal 'warning', config.log_level.name
    end
  end

  class GreeterTest < Minitest::Test
    def test_greets_by_name
      assert_equal 'Hello, ForgeBase!', Starter::Greeter.new.greet('ForgeBase')
    end

    def test_rejects_empty_names
      assert_raises(ArgumentError) { Starter::Greeter.new.greet('   ') }
    end
  end

  class LogSeverityTest < Minitest::Test
    def test_orders_by_severity_not_alphabetically
      assert_operator Starter::LogSeverity.parse('error'), :<,
                     Starter::LogSeverity.parse('information')
      assert_operator Starter::LogSeverity.parse('critical'), :<,
                     Starter::LogSeverity.parse('debug')
    end
  end
end
