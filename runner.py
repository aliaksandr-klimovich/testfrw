"""
This module provides classes to run test cases.
"""

from typing import Type

from case import TestCase
from event import ErrorEvent
from exception import AssertionFail, ComparisonError, TestFrwException
from logger import log
from result import TestResult, TestVerdict
from tb_info import get_tb_info


class TestRunner:
    """
    To run test cases.

    It is responsible to:
    1. Create test case instance and test result collector object.
    2. Establish communication channel between test case and test result class.
    3. Return test case run result.
    """

    @classmethod
    def run(cls, test_case: Type[TestCase]):

        test_result = TestResult()

        test_case_instance = test_case(test_result=test_result)

        try:
            test_case_instance.run()
        except AssertionFail:
            # verdict is updated before the exception is raised
            pass
        except ComparisonError:
            # verdict is updated before the exception is raised
            # log is made before the exception is raised
            pass
        except TestFrwException:
            # log is made before the exception is raised
            pass
        except:  # noqa
            tb_info = get_tb_info()
            test_result.events.append(ErrorEvent(tb_info=tb_info))
            test_result.update_verdict(TestVerdict.ERROR)

        log.info(f'test verdict: {test_result.verdict.name}')

        del test_case_instance

        return test_result
