import pytest

from starter.greeter import GreeterService


def test_greets_the_name():
    assert GreeterService().greet("World") == "Hello, World!"


def test_surrounding_whitespace_is_trimmed():
    assert GreeterService().greet("  World  ") == "Hello, World!"


@pytest.mark.parametrize("name", ["", "   "])
def test_empty_name_is_rejected(name):
    with pytest.raises(ValueError):
        GreeterService().greet(name)
