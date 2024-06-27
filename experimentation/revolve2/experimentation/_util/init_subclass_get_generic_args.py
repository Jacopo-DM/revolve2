from typing import Any, TypeVar, get_args, get_origin

TChild = TypeVar("TChild")
TParent = TypeVar("TParent")


def init_subclass_get_generic_args(
    child: type[TChild], parent: type[TParent]
) -> tuple[Any, ...]:
    """Get the generic arguments from a class within the __init_subclass__
    function.

    :param child: The type passed to the __init_subclass__ function.
    :type child: type[TChild]
    :param parent: The type of the parent class, which is the class
        __init_subclass__ is implemented for.
    :type parent: type[TParent]
    :returns: The types. Keep in mind these can be `ForwardRef`.
    :rtype: tuple[Any,...]

    """
    # find parent and its type annotations in the list of base classes of child
    orig_bases: list[type[TParent]] = [
        orig_base
        for orig_base in child.__orig_bases__  # type: ignore[attr-defined]
        if get_origin(orig_base) is parent
    ]  # TODO(jmdm): fix type annotation? possible?

    if len(orig_bases) >= 2:
        msg = "Implementer thinks this should be impossible. Expected that user can only inherit from parent class once."
        raise AssertionError(msg)

    orig_base = orig_bases[0]
    # get the generic types from the type annotations
    return get_args(orig_base)
