# -*- coding: utf-8 -*-
import allure
import pytest
from api_processor.wallet_model import transfer_out
from api_processor.wallet_model.wallet_list_page import WalletListPage
import Common.assert_tools as assert_tools
import Common.read_and_save_tool as config_tools
import ast
transfer_out = transfer_out.TransferOut()
assert_tools = assert_tools.AssertTools()
wallet_list_page = WalletListPage()
config_tools = config_tools.ConfigTools()

def get_params(case_name,section,key,send_amount = None):
    # 提前准备好测试参数
    currency_list = ['USDT', 'USDC']
    # 构建参数组合
    test_params = []
    for currency in currency_list:
        chains = ast.literal_eval(config_tools.get_value(section, key))

        for chain in chains:
            if send_amount is not None:

                test_params.append((case_name, currency, chain, send_amount))
            else:
                test_params.append((case_name, currency, chain))
    return test_params


test_payee_case_name = '钱包-获取加密收款地址列表'
@allure.epic("钱包模块")
@allure.feature("转出流程")
@pytest.mark.parametrize('test_case_name,from_currency,chain_name',get_params(test_payee_case_name, 'CHAIN_NAME', 'chain_name'))

@pytest.mark.priority("high")
def test_payee(test_case_name, http_request,from_currency,chain_name):
    """
    测试获取加密收款地址列表
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :return:
    """
    with allure.step(f"执行测试: {test_case_name}"):
        result = transfer_out.get_crypto_payee_data(test_case_name, http_request,from_currency,chain_name)
        assert_tools._common_response_validation_code(result, test_case_name)



def test_payee_id(http_request, from_currency = 'USDT', chain_name = 'arbitrum'):
    """
    测试获取加密收款地址列表
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :return:
    """
    with allure.step(f"执行测试: {test_payee_case_name}"):
        result = transfer_out._get_payee_id(http_request,from_currency,chain_name)




crypto_withdraw_fee_case_name = '钱包-转出费率'
@allure.epic("钱包模块")
@allure.feature("转出流程")
@pytest.mark.parametrize('test_case_name,from_currency', [
    (crypto_withdraw_fee_case_name,'USDT'),
    (crypto_withdraw_fee_case_name,'USDC'),
])
@pytest.mark.priority("high")
def test_crypto_withdraw_fee(test_case_name, http_request,from_currency):
    """
    测试加密资产转出功能
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :return:
    """
    with allure.step(f"执行测试: {test_case_name}"):
        result = transfer_out.get_crypto_withdraw_fee_data(test_case_name, http_request,from_currency)
        assert_tools._common_response_validation_code(result, test_case_name)










@allure.epic("钱包模块")
@allure.feature("转出流程")
@pytest.mark.parametrize('from_currency,chain_name,amount', [
    ('USDT','arbitrum','0.01'),

])
@pytest.mark.priority("high")
def test_transfer_data(http_request, from_currency, chain_name, amount):
    """
    测试加密资产转出功能
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :return:
    """
    with allure.step(f"执行测试: {transfer_out_case_name}"):
        result = transfer_out.transfer_out_data(http_request, from_currency, chain_name, amount)
        print(
            f"测试结果为：{result}"
        )
        # assert_tools._common_response_validation_code(result, test_case_name)

@allure.epic("钱包模块")
@allure.feature("转出流程")
@pytest.mark.parametrize('from_currency', [
    ('USDT'),
    ('USDC'),
])
def test_transfer_out_fee_data(http_request,from_currency):
    """
    测试获取转出手续费
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :return:
    """
    with allure.step(f"执行测试: {transfer_out_case_name}"):
        result = transfer_out.get_transfer_out_fee(http_request,from_currency)
        print(f"测试结果为：{result}")



transfer_out_handling_fee_case_name = '获取后台设置的转出手续费'
@allure.epic("钱包模块")
@allure.feature("转出流程")
@pytest.mark.parametrize('test_case_name,chain_name',
                         [(transfer_out_handling_fee_case_name,'arbitrum'),
                          (transfer_out_handling_fee_case_name,'polygon'),
                          (transfer_out_handling_fee_case_name,'avalanche'),
                          (transfer_out_handling_fee_case_name,'ethereum'),
                          (transfer_out_handling_fee_case_name,'bsc'),
                          (transfer_out_handling_fee_case_name, 'tron')
                          ])
def test_get_transfer_out_handling_fee(test_case_name, http_request,chain_name):
    """
    测试获取后台设置的转出手续费
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :return:
    """
    with allure.step(f"执行测试: {transfer_out_handling_fee_case_name}"):
        result = transfer_out._get_transfer_out_handling_fee(test_case_name, http_request,chain_name)
        print(f"测试结果为：{result}")


transfer_out_case_name = '钱包-加密资产转出_pass'
amount = 1.0
@allure.epic("钱包模块")
@allure.feature("转出流程")
@pytest.mark.parametrize('test_case_name,from_currency,chain_name,amount', get_params(transfer_out_case_name, 'CHAIN_NAME', 'chain_name',amount))

@pytest.mark.priority("high")
def test_transfer_out_pass( test_case_name, http_request, from_currency, chain_name, amount, before_wallet_data_out_type):
    """
    测试加密资产转出功能
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :return:
    """
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            variables = transfer_out.transfer_out_data(http_request, from_currency, chain_name, amount)
            result = transfer_out._transfer_out_pass(variables, test_case_name, http_request)
            assert_tools._common_response_validation_code(result, test_case_name)

            # 断言业务逻辑，转账后币种余额是否正确
            after_amount = wallet_list_page.get_currency_data(http_request, from_currency)
            handling_fee = transfer_out.transfer_out_handling_fee(http_request,chain_name,price=after_amount['price'])
            fee =  float(transfer_out.get_transfer_out_fee(http_request, from_currency)) + handling_fee
            assert_tools._common_response_validation_amount(
                currency=from_currency,
                before_amount=before_wallet_data_out_type,
                after_amount=after_amount,
                amount=amount,
                fee=fee,
                test_case_name=test_case_name,
                with_fee=True
            )

        except AssertionError as ae:
            allure.attach(f"断言失败: {str(ae)}", name="断言信息")
            raise
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise

transfer_out_case_name_fail= '钱包-加密资产转出_fail'
@allure.epic("钱包模块")
@allure.feature("转出流程")
@pytest.mark.parametrize('test_case_name,from_currency,chain_name,amount', [
    (transfer_out_case_name_fail,'USDT','arbitrum',0.1),
])

@pytest.mark.priority("high")
def test_transfer_out_fail( test_case_name, http_request, from_currency, chain_name, amount):
    """
    测试加密资产转出功能
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :return:
    """
    with allure.step(f"执行测试: {test_case_name}"):

        variables = transfer_out.transfer_out_data(http_request, from_currency, chain_name, amount)
        result = transfer_out._transfer_out_fail(variables, test_case_name, http_request)
        assert_tools._common_response_validation_code(result, test_case_name)





if __name__ == '__main__':
    pytest.main(["-s", "--env", "test", "--priority", "high", "--collect-only",
                 "/Users/alloyx/Desktop/alloxy_api_testcase_framework/TestCase/test_transfer_out.py"])
