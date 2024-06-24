"""Rerun a robot with given body and parameters."""

import logging
import pickle
from typing import TYPE_CHECKING

from evaluator import Evaluator
from revolve2.experimentation.logging import setup_logging

if TYPE_CHECKING:
    from individual import Individual

# This is a pickled genotype we optimized.
# You can copy your own parameters from the optimization output log.
PICKLED_GENOTYPE = b'\x80\x04\x95\x13\x1c\x00\x00\x00\x00\x00\x00\x8c\nindividual\x94\x8c\nIndividual\x94\x93\x94)\x81\x94}\x94(\x8c\x08genotype\x94h\x05\x8c\x08Genotype\x94\x93\x94)\x81\x94}\x94(\x8c\x05brain\x94\x8cFrevolve2.ci_group.genotypes.cppnwin._multineat_genotype_pickle_wrapper\x94\x8c\x1eMultineatGenotypePickleWrapper\x94\x93\x94)\x81\x94X\xf3\x08\x00\x00{\n"value0":{\n"value0":0,\n"value1":[\n{\n"value0":{\n"value0":[]\n},\n"value1":1,\n"value2":1,\n"value3":0.0,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":1,\n"value10":0.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":2,\n"value2":1,\n"value3":0.0,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":1,\n"value10":0.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":3,\n"value2":1,\n"value3":0.0,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":1,\n"value10":0.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":4,\n"value2":1,\n"value3":0.0,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":1,\n"value10":0.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":5,\n"value2":1,\n"value3":0.0,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":1,\n"value10":0.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":6,\n"value2":1,\n"value3":0.0,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":1,\n"value10":0.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":7,\n"value2":2,\n"value3":0.0,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":1,\n"value10":0.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":8,\n"value2":4,\n"value3":3.025,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":9,\n"value10":1.0\n}\n],\n"value2":[\n{\n"value0":{\n"value0":[]\n},\n"value1":1,\n"value2":8,\n"value3":1,\n"value4":false,\n"value5":0.44410939943909036\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":2,\n"value2":8,\n"value3":2,\n"value4":false,\n"value5":-0.7923416928227465\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":3,\n"value2":8,\n"value3":3,\n"value4":false,\n"value5":-0.23559896574924009\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":4,\n"value2":8,\n"value3":4,\n"value4":false,\n"value5":0.6895327746028656\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":5,\n"value2":8,\n"value3":5,\n"value4":false,\n"value5":-0.029969479179376036\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":6,\n"value2":8,\n"value3":6,\n"value4":false,\n"value5":-0.42692467058119457\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":7,\n"value2":8,\n"value3":7,\n"value4":false,\n"value5":0.85083216423555\n}\n],\n"value3":7,\n"value4":1,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0.0,\n"value9":false,\n"value10":16384,\n"value11":{\n"value0":[]\n},\n"value12":8,\n"value13":7\n}\n}\x94b\x8c\x04body\x94h\r)\x81\x94X5\x12\x00\x00{\n"value0":{\n"value0":0,\n"value1":[\n{\n"value0":{\n"value0":[]\n},\n"value1":1,\n"value2":1,\n"value3":0.0,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":1,\n"value10":0.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":2,\n"value2":1,\n"value3":0.0,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":1,\n"value10":0.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":3,\n"value2":1,\n"value3":0.0,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":1,\n"value10":0.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":4,\n"value2":1,\n"value3":0.0,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":1,\n"value10":0.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":5,\n"value2":2,\n"value3":0.0,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":1,\n"value10":0.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":6,\n"value2":4,\n"value3":3.025,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":2,\n"value10":1.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":7,\n"value2":4,\n"value3":3.025,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":2,\n"value10":1.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":8,\n"value2":4,\n"value3":3.025,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":2,\n"value10":1.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":9,\n"value2":4,\n"value3":3.025,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":2,\n"value10":1.0\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":10,\n"value2":4,\n"value3":3.025,\n"value4":0.0,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0,\n"value9":2,\n"value10":1.0\n}\n],\n"value2":[\n{\n"value0":{\n"value0":[]\n},\n"value1":1,\n"value2":6,\n"value3":1,\n"value4":false,\n"value5":-0.1535929984484911\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":2,\n"value2":6,\n"value3":2,\n"value4":false,\n"value5":-0.256040215980187\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":3,\n"value2":6,\n"value3":3,\n"value4":false,\n"value5":-0.11652438874716598\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":4,\n"value2":6,\n"value3":4,\n"value4":false,\n"value5":0.512759493936422\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":5,\n"value2":6,\n"value3":5,\n"value4":false,\n"value5":-0.291058484455749\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":1,\n"value2":7,\n"value3":6,\n"value4":false,\n"value5":0.3401051113311863\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":2,\n"value2":7,\n"value3":7,\n"value4":false,\n"value5":0.003701566667968309\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":3,\n"value2":7,\n"value3":8,\n"value4":false,\n"value5":-0.10693831461122142\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":4,\n"value2":7,\n"value3":9,\n"value4":false,\n"value5":-0.004312966387847603\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":5,\n"value2":7,\n"value3":10,\n"value4":false,\n"value5":-0.10322541810789601\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":1,\n"value2":8,\n"value3":11,\n"value4":false,\n"value5":0.22381602513220279\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":2,\n"value2":8,\n"value3":12,\n"value4":false,\n"value5":0.1258996280364242\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":3,\n"value2":8,\n"value3":13,\n"value4":false,\n"value5":0.6644527732983718\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":4,\n"value2":8,\n"value3":14,\n"value4":false,\n"value5":0.31167581639255706\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":5,\n"value2":8,\n"value3":15,\n"value4":false,\n"value5":0.07732642732133166\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":1,\n"value2":9,\n"value3":16,\n"value4":false,\n"value5":0.1886089429699378\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":2,\n"value2":9,\n"value3":17,\n"value4":false,\n"value5":-0.23850927321994046\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":3,\n"value2":9,\n"value3":18,\n"value4":false,\n"value5":-0.39291626265490389\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":4,\n"value2":9,\n"value3":19,\n"value4":false,\n"value5":0.9865525267487052\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":5,\n"value2":9,\n"value3":20,\n"value4":false,\n"value5":-0.26090421165293278\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":1,\n"value2":10,\n"value3":21,\n"value4":false,\n"value5":0.7791402018734168\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":2,\n"value2":10,\n"value3":22,\n"value4":false,\n"value5":0.10413948026852882\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":3,\n"value2":10,\n"value3":23,\n"value4":false,\n"value5":0.14350409990523678\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":4,\n"value2":10,\n"value3":24,\n"value4":false,\n"value5":-0.15528087437848304\n},\n{\n"value0":{\n"value0":[]\n},\n"value1":5,\n"value2":10,\n"value3":25,\n"value4":false,\n"value5":-0.7820723657814902\n}\n],\n"value3":5,\n"value4":5,\n"value5":0.0,\n"value6":0.0,\n"value7":0,\n"value8":0.0,\n"value9":false,\n"value10":16384,\n"value11":{\n"value0":[]\n},\n"value12":10,\n"value13":25\n}\n}\x94bub\x8c\x07fitness\x94G?\xda\x92\x97\xc5\xc9=.ub.'


def main() -> None:
    """Perform the rerun.

    :rtype: None

    """
    setup_logging()

    individual: Individual = pickle.loads(PICKLED_GENOTYPE)

    logging.info(f"Fitness from pickle: {individual.fitness}")

    evaluator = Evaluator(
        headless=False,
        num_simulators=1,
    )
    fitness = evaluator.evaluate([individual.genotype])[0]
    logging.info(f"Rerun fitness: {fitness}")


if __name__ == "__main__":
    main()
