from baby_steps import given, then, when
from pytest import raises

from district42 import Props, register_type, schema
from district42.types import Schema


def test_register_type():
    with given:
        class CustomType(Schema[Props]):
            def __accept__(self, visitor, **kwargs):
                pass

    with when:
        res = register_type("custom_type", CustomType)

    with then:
        assert isinstance(res, CustomType)
        assert isinstance(schema.custom_type, CustomType)
        assert schema.custom_type is not schema.custom_type


def test_register_incorrect_type():
    with given:
        class CustomIncorrectType:
            def __accept__(self, visitor, **kwargs):
                pass

    with when, raises(Exception) as exception:
        register_type("custom_incorrect_type", CustomIncorrectType)

    with then:
        assert exception.type is AssertionError
