"""Body Genotype Mapping for V1 Robot."""

from ci_group.genotypes.cppnwin.modular_robot.v1._body_develop import (
    develop as develop_body_v1,
)
from ci_group.genotypes.cppnwin.modular_robot.v1._body_genotype_orm_v1 import (
    BodyGenotypeOrmV1,
)
from ci_group.genotypes.cppnwin.modular_robot.v1._body_genotype_v1 import (
    BodyGenotypeV1,
)

__all__ = ["BodyGenotypeOrmV1", "BodyGenotypeV1", "develop_body_v1"]
