import json
import logging
import math
from decimal import Decimal

import allure
import pytest

from Common.get_set_decimals import Decimals


logger = logging.getLogger("log")
decimals = Decimals()


class AssertTools:
    """通用断言工具：集中处理状态码、余额和 Allure 断言附件。"""

    def assert_status_code(self, expected, actual, message="状态码断言失败"):
        # 中文备注：Excel 读取到的状态码可能是字符串或数字，统一转 int 后比较。
        expected = int(expected)
        actual = int(actual)
        with allure.step(f"断言状态码: expected={expected}, actual={actual}"):
            assert expected == actual, f"{message} - 预期: {expected}, 实际: {actual}"
        logger.info("状态码断言成功: expected=%s actual=%s", expected, actual)

    def assert_wallet_balance_equal(self, expected, actual, message="钱包余额断言失败"):
        with allure.step("断言钱包余额"):
            assert Decimal(str(expected)) == Decimal(str(actual)), (
                f"{message} - 预期余额: {expected}, 实际余额: {actual}"
            )

    def _attach_response_for_assert(self, response, test_case_name: str) -> None:
        if response is None:
            allure.attach("response is None", name=f"{test_case_name}-无响应", attachment_type=allure.attachment_type.TEXT)
            return
        allure.attach(str(response.status_code), name=f"{test_case_name}-实际状态码",
                      attachment_type=allure.attachment_type.TEXT)
        try:
            body = json.dumps(response.json(), ensure_ascii=False, indent=2)
            attachment_type = allure.attachment_type.JSON
        except ValueError:
            body = response.text
            attachment_type = allure.attachment_type.TEXT
        allure.attach(body[:10000], name=f"{test_case_name}-响应体", attachment_type=attachment_type)

    def _common_response_validation_code(self, result, test_case_name):
        # 中文备注：所有接口用例共用响应结构校验，避免每个测试函数重复写断言。
        with allure.step(f"校验接口响应: {test_case_name}"):
            if result is None or not isinstance(result, (tuple, list)) or len(result) != 4:
                allure.attach(str(result), name="返回结构异常", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"{test_case_name}接口调用失败，返回结果格式应为4元组")

            response, extracted_parameters, assert_code, case_id = result
            self._attach_response_for_assert(response, test_case_name)

            if response is None:
                pytest.fail(f"{test_case_name}接口无响应")
            if response.status_code is None:
                pytest.fail(f"{test_case_name}接口无响应状态码")

            try:
                self.assert_status_code(assert_code, response.status_code)
            except AssertionError as exc:
                pytest.fail(str(exc))
            return response, extracted_parameters, assert_code, case_id

    def _common_response_validation_amount(
        self, currency, before_amount, after_amount, amount, fee, test_case_name, with_fee=True
    ):
        with allure.step(f"校验钱包余额: {test_case_name}"):
            amount = abs(Decimal(str(amount)))
            fee = abs(Decimal(str(fee)))

            def parse_amount(value):
                if isinstance(value, dict):
                    if "amount" not in value:
                        raise ValueError("余额字典缺少amount字段")
                    value = value["amount"]
                return Decimal(str(value))

            before_decimal = parse_amount(before_amount)
            after_decimal = parse_amount(after_amount)
            total_deduction = amount + fee if with_fee else amount - fee
            expected_decimal = before_decimal - total_deduction
            expected = float(decimals._get_decimals_for_crypto(currency, decimal_str=float(expected_decimal)))

            allure.attach(
                json.dumps(
                    {
                        "currency": currency,
                        "before": str(before_decimal),
                        "after": str(after_decimal),
                        "amount": str(amount),
                        "fee": str(fee),
                        "expected": expected,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                name="余额断言上下文",
                attachment_type=allure.attachment_type.JSON,
            )
            if not math.isclose(expected, float(after_decimal), rel_tol=1e-9):
                pytest.fail(f"{test_case_name}钱包金额断言失败: 期望{expected}, 实际{after_decimal}")
