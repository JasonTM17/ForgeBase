# frozen_string_literal: true

# Fail-fast startup validation: the Rails process refuses to boot on a
# broken deployment configuration so misconfiguration is never discovered
# through request traffic.
#
# Explicitly require the library first: lib/forgebase is autoloaded by
# config.autoload_lib, but initializers run before autoloaded constants
# are guaranteed to be defined, so a direct reference here would otherwise
# raise NameError during boot.

require_relative '../../lib/forgebase/config'
require_relative '../../lib/forgebase/log_severity'

Rails.application.config.forgebase = Forgebase::Config.load_from_environment!
