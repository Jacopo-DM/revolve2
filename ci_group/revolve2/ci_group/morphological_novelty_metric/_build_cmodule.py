import os
from pathlib import Path

import numpy as np
from Cython.Build import cythonize
from setuptools import Extension, setup


def build() -> None:
    """Build the morphological novelty shared object.

    :rtype: None

    :raises OSError: If the users OS is not Windows or UNIX-based.

    """
    file_path = Path(__file__).resolve()
    directory_path = file_path.parent

    source = str(directory_path / "_calculate_novelty.pyx")
    include = np.get_include()

    match os.name:
        case "nt":  # Windows
            extra_compile_args = [
                "/O2",
                "-UNDEBUG",
            ]
        case "posix":  # UNIX-based systems
            extra_compile_args = [
                "-O3",
                "-ffast-math",
                "-UNDEBUG",
            ]
        case _:
            msg = f"No build parameter set for operating systems of type {os.name}"
            raise OSError(msg)

    ext = Extension(
        name="calculate_novelty",
        sources=[source],
        include_dirs=[include],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
        extra_compile_args=extra_compile_args,
    )

    ext_modules = cythonize(
        ext,
        include_path=[include],
        compiler_directives={"binding": True, "language_level": 3},
    )

    setup(
        ext_modules=ext_modules,
        script_args=["build_ext", f"--build-lib={directory_path}"],
    )


if __name__ == "__main__":
    build()
