import traceback
from typing import Callable, Optional

import allure
import pytest

from Common import logger
from Common.assert_tools import AssertTools
from Common.response_assertion import ResponseAssertion


logger = logger.logger


class CaseRunner:
    """测试用例统一执行器。

    中文备注：把测试函数里重复的 allure.step、异常捕获、响应断言、pytest.fail
    收敛到一个地方，避免测试代码只 attach 不 fail 造成假通过。
    """

    def __init__(self, assert_tools: Optional[AssertTools] = None):
        self.assert_tools = assert_tools or AssertTools()

    def run_api_case(
        self,
        case_name: str,
        func: Callable,
        *args,
        response_rules: Optional[list[dict]] = None,
        **kwargs,
    ):
        """执行一个接口用例并返回通用校验后的结果。"""
        with allure.step(f"执行测试: {case_name}"):
            try:
                result = func(*args, **kwargs)
                response, extracted, assert_code, case_id = self.assert_tools._common_response_validation_code(
                    result, case_name
                )
                ResponseAssertion.assert_response_rules(response, response_rules)
                return response, extracted, assert_code, case_id
            except AssertionError:
                # 中文备注：断言异常保留原始堆栈，方便 pytest 明确标记失败。
                logger.exception("用例断言失败: %s", case_name)
                allure.attach(traceback.format_exc(), name="断言异常堆栈", attachment_type=allure.attachment_type.TEXT)
                raise
            except Exception as exc:
                logger.exception("用例执行异常: %s", case_name)
                allure.attach(traceback.format_exc(), name="执行异常堆栈", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"{case_name} 执行失败: {exc}")


case_runner = CaseRunner()
