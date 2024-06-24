from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    ForwardRef,
    Generic,
    Self,
    TypeVar,
)

import sqlalchemy.ext.orderinglist
from sqlalchemy import orm

from ..._util.init_subclass_get_generic_args import (
    init_subclass_get_generic_args,
)
from ...database import HasId

TIndividual = TypeVar("TIndividual")


class Population(HasId, orm.MappedAsDataclass, Generic[TIndividual]):
    """Generic SQLAlchemy model for a population.

    Inherit from this to create your own population type.

    The generic parameter `TIndividual` refers to the user-defined individual type.
    This parameter cannot be a forward reference.

    For example::

        class MyPopulation(Base, Population[MyIndividual]):
            __tablename__ = "my_population"

    Attributes:
        individuals (orm.Mapped[list[TIndividual]]): A mapped relationship to the individuals in the population.
            This attribute is interesting to the user and can be accessed directly.
    """

    # -------------------------------------
    # Class members interesting to the user
    # -------------------------------------
    if TYPE_CHECKING:
        individuals: orm.Mapped[list[TIndividual]]

    # ----------------------
    # Implementation details
    # ----------------------
    else:

        @orm.declared_attr
        def individuals(self) -> orm.Mapped[list[TIndividual]]:
            """Return a list of individuals in the population.

            :return: A list of individuals.
            """
            return self.__individuals_impl()

    __type_tindividual: ClassVar[type[TIndividual]]  # type: ignore[misc]

    def __init_subclass__(cls: type[Self], /, **kwargs: dict[str, Any]) -> None:
        """Initialize a version of this class when it is subclassed.

        Gets the actual type of `TIndividual` and stores it for later use.

        :param kwargs: Remaining arguments passed to super.
        """
        generic_types = init_subclass_get_generic_args(cls, Population)
        if len(generic_types) != 1:
            msg = f"Expected exactly one generic argument for {cls.__name__}, got {len(generic_types)}."
            raise ValueError(msg)

        cls.__type_tindividual = generic_types[0]
        if isinstance(cls.__type_tindividual, ForwardRef):
            msg = "TIndividual generic argument cannot be a forward reference."
            raise TypeError(msg)

        # TODO(jmdm): Fix type annotation?
        super().__init_subclass__(**kwargs)  # type: ignore[arg-type]

    @classmethod
    def __individuals_impl(cls) -> orm.Mapped[TIndividual]:
        """Return the relationship to the individuals in the population.

        This method defines the relationship between the population and its individuals.
        It returns a relationship object that represents the mapping between the population
        and the individuals.

        :return: The relationship object representing the individuals in the population.
        :rtype: orm.Mapped[TIndividual]
        """
        return orm.relationship(
            cls.__type_tindividual,
            order_by=cls.__type_tindividual.population_index,
            collection_class=sqlalchemy.ext.orderinglist.ordering_list(
                "population_index"
            ),
        )
