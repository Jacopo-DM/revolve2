from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    ForwardRef,
    Generic,
    Self,
    TypeVar,
)

import sqlalchemy
from revolve2.experimentation._util.init_subclass_get_generic_args import (
    init_subclass_get_generic_args,
)
from revolve2.experimentation.database import HasId
from sqlalchemy import orm

TPopulation = TypeVar("TPopulation")


class Generation(HasId, orm.MappedAsDataclass, Generic[TPopulation]):
    """
    Generic SQLAlchemy model for a generation.

    Inherit from this to create your own generation type and table.

    The generic parameter `TPopulation` refers to the user-defined population type.
    This parameter cannot be a forward reference.

    For example::

        class MyGeneration(Base, Generation[MyPopulation]):
            __tablename__ = "my_generation"
    """

    # -------------------------------------
    # Class members interesting to the user
    # -------------------------------------
    if TYPE_CHECKING:
        generation_index: orm.Mapped[int] = orm.mapped_column(
            nullable=False, unique=True
        )
        _population_id: orm.Mapped[int] = orm.mapped_column(
            "population_id",
            sqlalchemy.ForeignKey("population.id"),
            nullable=False,
            init=False,
        )
        population: orm.Mapped[TPopulation] = orm.relationship()

    # ----------------------
    # Implementation details
    # ----------------------
    else:

        @orm.declared_attr
        def generation_index(self) -> orm.Mapped[int]:
            return self.__generation_index_impl()

        @orm.declared_attr
        def _population_id(self) -> orm.Mapped[int]:
            return self.__population_id_impl()

        @orm.declared_attr
        def population(self) -> orm.Mapped[TPopulation]:
            return self.__population_impl()

    __type_tpopulation: ClassVar[type[TPopulation]]

    def __init_subclass__(cls: type[Self], /, **kwargs: dict[str, Any]) -> None:
        """
        Initialize a version of this class when it is subclassed.

        Gets the actual type of `TPopulation` and stores it for later use.
        :param kwargs: Remaining arguments passed to super.
        """
        generic_types = init_subclass_get_generic_args(cls, Generation)
        if len(generic_types) != 1:
            msg = "Generation must have exactly one generic argument."
            raise ValueError(msg)
        cls.__type_tpopulation = generic_types[0]
        if not isinstance(cls.__type_tpopulation, ForwardRef):
            msg = "TPopulation generic argument cannot be a forward reference."
            raise TypeError(msg)

        super().__init_subclass__(**kwargs)

    @classmethod
    def __generation_index_impl(cls) -> orm.Mapped[int]:
        return orm.mapped_column(nullable=False, unique=True)

    @classmethod
    def __population_id_impl(cls) -> orm.Mapped[int]:
        return orm.mapped_column(
            sqlalchemy.ForeignKey(f"{cls.__type_tpopulation.__tablename__}.id"),
            nullable=False,
            init=False,
        )

    @classmethod
    def __population_impl(cls) -> orm.Mapped[TPopulation]:
        return orm.relationship(cls.__type_tpopulation)
