import numpy as np
import numpy.typing as npt
from sqlalchemy import event, orm
from sqlalchemy.engine import Connection


class Parameters(orm.MappedAsDataclass):
    """An SQLAlchemy mixing that provides a parameters column that is a tuple
    of floats.

    The parameters are saved in the database as string of semicolon
    separated floats.


    """

    parameters: npt.NDArray[np.float64]

    _serialized_parameters: orm.Mapped[str] = orm.mapped_column(
        "serialized_parameters", init=False, nullable=False
    )


@event.listens_for(Parameters, "before_update", propagate=True)
@event.listens_for(Parameters, "before_insert", propagate=True)
def _update_serialized_parameters(
    mapper: orm.Mapper[Parameters],
    connection: Connection,
    target: Parameters,
) -> None:
    """:param mapper:
    :type mapper: orm.Mapper[Parameters]
    :param connection:
    :type connection: Connection
    :param target:
    :type target: Parameters
    :rtype: None

    """
    target._serialized_parameters = ";".join(str(p) for p in target.parameters)


@event.listens_for(Parameters, "load", propagate=True)
def _deserialize_parameters(
    target: Parameters, context: orm.QueryContext
) -> None:
    """:param target:
    :type target: Parameters
    :param context:
    :type context: orm.QueryContext
    :rtype: None

    """
    target.parameters = np.array([
        float(p) for p in target._serialized_parameters.split(";")
    ])
