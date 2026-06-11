"""
断言操作
    断言响应状态码
    断言钱包余额
"""
from multiprocessing.context import assert_spawning

import allure
import logging
import pytest
import math
from decimal import Decimal
from Common.get_set_decimals import Decimals
logger = logging.getLogger('log')
decimals = Decimals()
class AssertTools:
    def assert_status_code(self, expected, actual, message="状态码断言失败"):
        """
        断言响应状态码是否符合预期
        :param expected: 预期状态码
        :param actual: 实际状态码
        :param message: 断言失败时的提示信息
        """
        assert expected == actual, f"{message} - 预期: {expected}, 实际: {actual}"
        logger.info(f"状态码断言成功：预期 {expected}，实际 {actual}")

    def assert_wallet_balance_equal(self, expected, actual, message="钱包余额断言失败"):
        """
        断言钱包金额是否等于预期值
        :param expected: 预期值
        :param actual: 实际值
        :param message: 断言失败时的提示信息
        """
        assert expected == actual, f"{message} - 预期余额: {expected}, 实际余额: {actual}"
        logger.info(f"钱包余额断言成功：预期 {expected}，实际 {actual}")

    def _common_response_validation_code(self, result, test_case_name):
        """
        通用响应验证函数
        :param result: 接口返回结果
        :param test_case_name: 测试用例名称

        """
        # 检查函数是否正常返回
        if result is None or len(result) != 4:
            allure.attach(f"{test_case_name}接口调用失败", name=f"{test_case_name}异常")
            pytest.fail(f"{test_case_name}接口调用失败，返回结果格式不正确")

        # 解包返回结果
        response, extracted_parameters, assert_code, case_id = result

        # 检查响应状态码是否存在
        if response.status_code is None:
            allure.attach("无响应状态码", name=f"{test_case_name}异常")
            pytest.fail(f"{test_case_name}接口无响应状态码")

        # 检查响应状态码是否与断言状态码一致
        try:
            self.assert_status_code(assert_code, response.status_code)
            allure.attach(str(response.status_code), name=f"{test_case_name}成功状态码")
        except AssertionError:
            allure.attach(str(response.status_code), name="状态码断言失败")
            pytest.fail(f"状态码断言失败: 期望{assert_code}, 实际{response.status_code}")

        return response, extracted_parameters, assert_code, case_id

    def _common_response_validation_amount(self, currency, before_amount, after_amount, amount, fee, test_case_name,
                                           with_fee=True):
        """
        通用钱包余额验证函数
        :param before_amount: 转账前金额
        :param after_amount: 转账后金额
        :param amount: 转账金额
        :param fee: 手续费
        :param test_case_name: 测试用例名称
        :param with_fee: 是否包含手续费计算，默认True（即总扣除=amount+fee）
        """

        # 数据预处理
        amount = abs(Decimal(str(amount)))
        fee = abs(Decimal(str(fee)))

        def parse_amount(val):
            if isinstance(val, dict):
                if 'amount' not in val:
                    raise ValueError("Amount dictionary must contain 'amount' key.")
                return Decimal(str(val['amount']))
            return Decimal(str(val))

        before_amount = parse_amount(before_amount.get('amount',0))
        after_amount = parse_amount(after_amount)

        # 计算预期余额
        total_deduction = amount + fee if with_fee else amount - fee
        expected_decimal = before_amount - total_deduction

        # 使用 decimals._get_decimals_for_crypto 处理精度（假设其返回字符串形式的小数）
        expected_str = decimals._get_decimals_for_crypto(currency, decimal_str=float(expected_decimal))
        expected_amount = float(expected_str)

        # 断言并记录日志
        try:
            if not math.isclose(expected_amount, float(after_amount), rel_tol=1e-9):
                raise AssertionError(f"Expected {expected_amount}, but got {after_amount}")
            allure.attach(f"{test_case_name}成功", name=f"{test_case_name}成功")
        except AssertionError:
            allure.attach(f"{test_case_name}失败", name=f"{test_case_name}失败")
            pytest.fail(f"{test_case_name}钱包金额断言失败: 期望{expected_amount}, 实际{after_amount}")


