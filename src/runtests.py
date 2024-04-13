"""
Simple testing suite.
"""
from typing import Any, Callable
import evo.gtrees as gtrees
import evo.strees as strees
import os.path, sys
import logging

def run_test(test_no: int, test_fn: Callable[[str], Any], log: logging.Logger, iters: int = 1, against: Any = None) -> bool:
    """
    Runs test `test_no` on `test_fn` and compares it against `against`.
    If `against` is not provided, then `run_test` will return true iff execution
    finishes without errors. If `against` is provided, `run_test` will return the
    result of __eq__ on the output of `test_fn` with `against`. All exceptions
    are caught and logged to `log`, so as to not interrupt the test suite.
    :param int test_no The test to run
    :param Callable[[str], Any] test_fn The test function callable
    :param logging.Logger Exceptions and status updates will be logged here
    :param Any against The expected output of `test_fn` on `test_no`
    :param int iters Number of times to run this test
    """
    test_input: str
    test_path: str = os.path.join("src/tests", f"test{str(test_no).zfill(2)}.txt")
    log.info(f"Running test #{test_no}: {test_path}")
    # open test file and read in its contents
    with open(test_path, "r") as tfile:
        test_input = tfile.read()
    result: Any
    failure: bool = False
    for iter in range(iters):
        log.info(f"Iteration {iter}...")
        try:
            result = test_fn(test_input)
        except Exception as e:
            failure = True
            logging.exception(repr(e))
        if against is not None:
            if result != against:
                failure = True
                logging.warning(f"Output:\n{result}\n" +
                                f"does not match expected:\n{against}")
            else:
                logging.info("Output matched expected result!")
    if failure:
        logging.info("One or more iterations failed.")
    else:
        logging.info("Test case passed!")
    return not failure

def create_and_print_tree(j: str):
    t = gtrees.GeneTree(j)
    print(t)

if __name__ == "__main__":
    # setup
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # run tests
    run_test(1, create_and_print_tree, logger, 1)