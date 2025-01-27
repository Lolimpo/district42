from typing import Any, Type, TypeVar, cast

from ._from_native import from_native
from ._props import Props
from ._schema_facade import SchemaFacade
from ._schema_visitor import SchemaVisitor, SchemaVisitorReturnType
from ._version import version
from .representor import Representor
from .types import AnySchema, GenericSchema, Schema, make_required, optional

__version__ = version
__all__ = ("schema", "GenericSchema", "Props", "SchemaVisitor", "SchemaVisitorReturnType",
           "from_native", "optional", "register_type", "represent", "make_required", )


schema = SchemaFacade()
_representor = Representor()

_SchemaType = TypeVar("_SchemaType", bound=GenericSchema)


def register_type(name: str, schema_type: Type[_SchemaType]) -> _SchemaType:
    assert issubclass(schema_type, Schema)
    setattr(SchemaFacade, name, property(lambda self: schema_type()))
    return cast(_SchemaType, getattr(schema, name))


def represent(self: GenericSchema, **kwargs: Any) -> str:
    return self.__accept__(_representor, **kwargs)


def union(self: GenericSchema, other: Any) -> AnySchema:
    return schema.any(self, other)


Schema.__override__("__repr__", represent)
Schema.__override__("__or__", union)
