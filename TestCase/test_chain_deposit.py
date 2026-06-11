# -*- coding: utf-8 -*-
import allure
import pytest
import Common.assert_tools as assert_tools
from api_processor.wallet_model import recharge
from Common.read_and_save_tool import ConfigTools
import ast

recharge = recharge.Recharge()
assert_tools = assert_tools.AssertTools()
config_tools = ConfigTools()

# 提前准备好测试参数
currency_list = ['USDT', 'USDC']
chain_deposit_case_name = '钱包-获取币种/链对应的钱包地址'

# 构建参数组合
test_params = []
for currency in currency_list:
    chains = ast.literal_eval(config_tools.get_value('CHAIN_NAME', 'chain_name'))

    for chain in chains:
        test_params.append((chain_deposit_case_name, currency, chain))

@allure.epic("钱包模块")
@allure.feature("链上充值")
@pytest.mark.priority("high")
@pytest.mark.parametrize('test_case_name,currency,chain_name', test_params)
def test_chain_deposit(test_case_name, http_request, currency,chain_name):
    """
    测试获取币种/链对应的钱包地址
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :param chain_name: 链名称
    :param currency: 币种
    :return:
    """
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = recharge.chain_deposit(test_case_name, http_request, currency, chain_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_chain_deposit.py'])