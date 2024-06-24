from copy import deepcopy

import multineat
from revolve2.ci_group.genotypes.cppnwin.modular_robot import (
    MultiNEATParamsWriter,
    ParamAnalyzer,
    get_multineat_params,
)

if __name__ == "__main__":
    # Get the parameters
    params = get_multineat_params()

    # Strip of pre-defined parameters
    param_writer = MultiNEATParamsWriter()
    params = param_writer.strip_params(params)

    # Analyze the parameters
    a1 = ParamAnalyzer(params=deepcopy(multineat.Parameters()))
    a2 = ParamAnalyzer(params=params)
    a2.print_multineat_params_full()
    a2.print_multineat_params_with_ref(a1)
    a2 - a1
