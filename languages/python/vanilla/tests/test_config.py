import pytest

from starter.config import VALID_ENVIRONMENTS, VALID_LOG_LEVELS, AppConfig, ConfigError


def test_defaults_are_development_safe():
    config = AppConfig.from_env(env={})
    assert config.app_name == "forgebase-vanilla"
    assert config.app_env == "development"
    assert config.log_level == "INFO"


def test_environment_overrides_apply():
    config = AppConfig.from_env(
        env={"APP_NAME": "my-app", "APP_ENV": "production", "LOG_LEVEL": "debug"}
    )
    assert config == AppConfig(app_name="my-app", app_env="production", log_level="DEBUG")


@pytest.mark.parametrize(
    "field,value",
    [
        ("APP_NAME", ""),
        ("APP_NAME", "   "),
        ("APP_ENV", "staging"),
        ("LOG_LEVEL", "verbose"),
    ],
)
def test_invalid_values_fail_fast(field, value):
    env = {field: value}
    with pytest.raises(ConfigError):
        AppConfig.from_env(env=env)


def test_error_documents_allowed_values():
    with pytest.raises(ConfigError) as excinfo:
        AppConfig.from_env(env={"APP_ENV": "staging"})
    assert str(VALID_ENVIRONMENTS) in str(excinfo.value)
    with pytest.raises(ConfigError) as excinfo:
        AppConfig.from_env(env={"LOG_LEVEL": "verbose"})
    assert str(VALID_LOG_LEVELS) in str(excinfo.value)


def test_config_is_immutable():
    config = AppConfig.from_env(env={})
    with pytest.raises(AttributeError):
        config.app_name = "changed"  # type: ignore[misc]
