import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from ._open_method import OpenMethod


def open_async_database_sqlite(
    db_file: str, open_method: OpenMethod = OpenMethod.OPEN_IF_EXISTS
) -> AsyncEngine:
    """Open an SQLAlchemy SQLite async database.

    :param db_file: File for the database.
    :type db_file: str
    :param open_method: The way the database should be opened. (Default value = OpenMethod.OPEN_IF_EXISTS)
    :type open_method: OpenMethod
    :returns: The opened database.
    :rtype: AsyncEngine

    """
    __common(db_file, open_method)
    return create_async_engine(f"sqlite+aiosqlite:///{db_file}")


def open_database_sqlite(
    db_file: str, open_method: OpenMethod = OpenMethod.OPEN_IF_EXISTS
) -> Engine:
    """Open an SQLAlchemy SQLite database.

    :param db_file: File for the database.
    :type db_file: str
    :param open_method: The way the database should be opened. (Default value = OpenMethod.OPEN_IF_EXISTS)
    :type open_method: OpenMethod
    :returns: The opened database.
    :rtype: Engine

    """
    __common(db_file, open_method)
    return create_engine(f"sqlite:///{db_file}")


def __common(
    db_file: str, open_method: OpenMethod = OpenMethod.OPEN_IF_EXISTS
) -> None:
    exists = os.path.exists(db_file)
    if open_method == OpenMethod.OPEN_IF_EXISTS:
        if not exists:
            msg = f"Open check set to OPEN_IF_EXISTS and database does not exist: {db_file}"
            raise RuntimeError(msg)
    elif open_method == OpenMethod.OPEN_OR_CREATE:
        os.makedirs(Path(db_file).parent, exist_ok=True)
    elif open_method == OpenMethod.NOT_EXISTS_AND_CREATE:
        if exists:
            msg = f"Open check set to NOT_EXISTS_AND_CREATE and database exists: {db_file}"
            raise RuntimeError(msg)
        os.makedirs(Path(db_file).parent, exist_ok=True)
    elif open_method == OpenMethod.OVERWRITE_IF_EXISTS:
        if exists:
            os.remove(db_file)
        else:
            os.makedirs(Path(db_file).parent, exist_ok=True)
