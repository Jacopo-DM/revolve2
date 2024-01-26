"""Functions to work with logging in a standardized way."""

import logging
from dataclasses import dataclass


@dataclass
class Clr:
    """Color palette for printing in the terminal."""

    # === Normal === #
    # Shades
    wh: str = "\033[97m"
    gr: str = "\033[90m"
    bk: str = "\033[30m"

    # RGB
    r: str = "\033[91m"
    g: str = "\033[92m"
    b: str = "\033[94m"

    # CYMK
    c: str = "\033[96m"
    m: str = "\033[95m"
    y: str = "\033[93m"

    # === Bold === #
    # Shades
    WH: str = "\033[1;97m"
    GR: str = "\033[1;90m"
    BK: str = "\033[1;30m"

    # RGB
    R: str = "\033[1;91m"
    G: str = "\033[1;92m"
    B: str = "\033[1;94m"

    # CYMK
    C: str = "\033[1;96m"
    M: str = "\033[1;95m"
    Y: str = "\033[1;93m"

    # === Styles === #
    EM = "\033[1m"  # Bold
    NEM = "\033[2m"  # Dim
    IT = "\033[3m"  # Italic
    UN = "\033[4m"  # Underline

    # === Functional === #
    E: str = "\033[0m"  # End


def setup_logging(level: int = logging.INFO, file_name: str | None = None) -> None:
    """
    Set up logging.

    :param level: The log level to use.
    :param file_name: If not None, also writes to this file.
    """
    # Set up logging.
    # Each message has an associated 'level'.
    # By default, we are interested in messages of level 'info' and the more severe 'warning', 'error', and 'critical',
    # and we exclude the less severe 'debug'.
    # Furthermore, we specify the format in which we want the messages to be printed.
    logging.basicConfig(
        level=level,
        format=f" [%(asctime)s] [%(levelname)s] {Clr.NEM}[%(module)s]{Clr.E} %(message)s",
        datefmt="%H:%M:%S",
    )
    # Add color to logging levels
    logging.addLevelName(logging.DEBUG, f"{Clr.GR}DEBUG{Clr.E}")
    logging.addLevelName(logging.INFO, f"{Clr.G}INFO{Clr.E}")
    logging.addLevelName(logging.WARNING, f"{Clr.Y}WARN{Clr.E}")
    logging.addLevelName(logging.ERROR, f"{Clr.R}ERROR{Clr.E}")

    if file_name is not None:
        logging.root.handlers.append(logging.FileHandler(file_name))

    bar = "=" * 40
    space = " " * (len(bar) // 4)
    for _ in range(3):
        logging.info(bar)
    logging.info(f"{space}New Log Starts Here")
    for _ in range(3):
        logging.info(bar)
