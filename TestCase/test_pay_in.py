# -*- coding: utf-8 -*-
import allure
import pytest
from Common.read_and_save_tool import ConfigTools
from api_processor.wallet_model.pay_in import PayIn
import Common.assert_tools as assert_tools



pay_in = PayIn()
assert_tools = assert_tools.AssertTools()
config = ConfigTools()




def get_params(case_name, type, key_name: list[str] = None, include_amount=False):
    """
    获取测试参数列表

    Args:
        case_name: 测试用例名称
        type: 数据类型
        key_name: 键名列表
        include_amount: 是否包含金额参数

    Returns:
        list: 测试参数列表
    """
    test_params_list = []
    currency_list = ['USDT', 'USDC']
    values = config.get_yellow_card_data(type, key_name)

    if values is None:
        return test_params_list

    for to_currency in currency_list:
        for value in values:
            if include_amount and len(value) >= 2:
                # 包含金额参数的情况：(case_name, currency, to_currency, amount)
                test_params_list.append((case_name, value[0], to_currency, value[1]))
            elif len(value) >= 1:
                # 不包含金额参数的情况：(case_name, currency, to_currency)
                test_params_list.append((case_name, value[0], to_currency))
    print(test_params_list)
    return test_params_list


@allure.epic("钱包模块")
@allure.feature("pay_in模块")
@pytest.mark.parametrize('test_case_name', [
    '获取国家信息'
])
@pytest.mark.priority("high")
def test_get_country_info(test_case_name,http_request):
    """
    测试获取国家信息
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :return:
    """
    with allure.step(f"执行获取国家信息测试: {test_case_name}"):
        result = pay_in.get_country_info(http_request,test_case_name)
        assert_tools._common_response_validation_code(result, test_case_name)



@allure.epic("钱包模块")
@allure.feature("pay_in模块")
@pytest.mark.parametrize('test_case_name', [
    '获取法币到加密货币手续费'
])
@pytest.mark.priority("high")
def test_get_fiat_in_fee(test_case_name,http_request):
    """
    测试获取法币到加密货币手续费
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :return:
    """
    with allure.step(f"执行获取法币到加密货币手续费测试: {test_case_name}"):
        result = pay_in.get_fiat_in_fee(http_request,test_case_name)
        assert_tools._common_response_validation_code(result, test_case_name)





pay_in_fee_case_name = '钱包-获取汇率'
@allure.epic("钱包模块")
@allure.feature("pay_in模块")
@pytest.mark.parametrize('test_case_name, from_currency, to_currency',
                         get_params(pay_in_fee_case_name, 'payin', ['currency'], include_amount=False))
@pytest.mark.priority("high")
def test_get_pay_in_fee(test_case_name, http_request, from_currency, to_currency):
    """
    测试获取法币到加密货币手续费
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :return:
    """
    with allure.step(f"执行获取法币到加密货币手续费测试: {test_case_name}"):
        result = pay_in.get_pay_in_fee(http_request,test_case_name,from_currency, to_currency)
        assert_tools._common_response_validation_code(result, test_case_name)






PAY_IN_SUBMIT_CASE_NAME = '钱包-提交payin请求_PASS'


@allure.epic("钱包模块")
@allure.feature("pay_in模块")
@pytest.mark.parametrize(
    'test_case_name, from_currency, to_currency, amount',
    get_params(PAY_IN_SUBMIT_CASE_NAME, 'payin', ['currency', 'min_limit'], include_amount=True)
)
def test_pay_in_submit(test_case_name, http_request, from_currency, to_currency, amount):
    """
    测试提交payin请求
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :return:
    """
    with allure.step(f"执行提交payin请求测试: {test_case_name}"):
        try:
            variables = pay_in.pay_in_parameter(http_request, from_currency, to_currency, amount)
            if variables is None:
                return None
            result = pay_in.pay_in_submit(variables, test_case_name, http_request, from_currency, to_currency, amount)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(str(e), name="异常详情", attachment_type=allure.attachment_type.TEXT)
            raise






if __name__ == '__main__':
    pytest.main(['-s', 'test_pay_in.py'])