"""Body Genotype Mapping for V1 Robot."""

from ci_group.genotypes.cppnwin.modular_robot.v2._body_develop import (
    develop as develop_body_v2,
)
from ci_group.genotypes.cppnwin.modular_robot.v2._body_genotype_orm_v2 import (
    BodyGenotypeOrmV2,
)
from ci_group.genotypes.cppnwin.modular_robot.v2._body_genotype_v2 import (
    BodyGenotypeV2,
)

__all__ = ["BodyGenotypeOrmV2", "BodyGenotypeV2", "develop_body_v2"]
