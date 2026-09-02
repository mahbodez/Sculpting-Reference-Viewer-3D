"""Tolerant conversion between dataclasses and plain JSON structures.

Sessions written by an older build must keep opening in a newer one, so
:func:`decode` ignores unknown keys and falls back to field defaults for
anything missing or malformed.
"""

from __future__ import annotations

import dataclasses
import types
import typing
from enum import Enum

import numpy as np

T = typing.TypeVar("T")


def encode(value: typing.Any) -> typing.Any:
    """Convert dataclasses, enums, tuples and numpy arrays to JSON types."""
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {f.name: encode(getattr(value, f.name)) for f in dataclasses.fields(value)}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    if isinstance(value, dict):
        return {str(key): encode(item) for key, item in value.items()}
    return value


def decode(cls: type[T], data: typing.Any) -> T:
    """Build an instance of the dataclass ``cls`` from ``data``."""
    if not dataclasses.is_dataclass(cls):
        raise TypeError(f"{cls!r} is not a dataclass")
    if not isinstance(data, dict):
        return cls()  # type: ignore[call-arg]

    hints = typing.get_type_hints(cls)
    kwargs: dict[str, typing.Any] = {}
    for field in dataclasses.fields(cls):
        if field.name not in data:
            continue
        try:
            kwargs[field.name] = _coerce(hints.get(field.name, typing.Any), data[field.name])
        except (TypeError, ValueError):
            continue  # Keep the field default rather than failing the load.
    return cls(**kwargs)  # type: ignore[call-arg]


def _coerce(annotation: typing.Any, value: typing.Any) -> typing.Any:
    if annotation is typing.Any:
        return value
    if dataclasses.is_dataclass(annotation):
        return decode(annotation, value)
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return annotation(value)

    origin = typing.get_origin(annotation)
    if origin is tuple:
        args = typing.get_args(annotation)
        item_type = args[0] if args else typing.Any
        return tuple(_coerce(item_type, item) for item in value)
    if origin is list:
        args = typing.get_args(annotation)
        item_type = args[0] if args else typing.Any
        return [_coerce(item_type, item) for item in value]
    if origin is typing.Union or origin is getattr(types, "UnionType", None):
        for candidate in typing.get_args(annotation):
            if candidate is type(None):
                if value is None:
                    return None
                continue
            try:
                return _coerce(candidate, value)
            except (TypeError, ValueError):
                continue
        return value

    if annotation is bool:
        return bool(value)
    if annotation is float:
        return float(value)
    if annotation is int:
        return int(value)
    if annotation is str:
        return str(value)
    return value
