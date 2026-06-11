# -*- coding: utf-8 -*-
import allure
import pytest
from api_processor.wallet_model import wallet_list_page
import Common.assert_tools as assert_tools
from Common.read_and_save_tool import ConfigTools
import ast

wallet_list_page = wallet_list_page.WalletListPage()
assert_tools = assert_tools.AssertTools()
config_tools = ConfigTools()

@allure.epic("钱包模块")
@allure.feature("前置流程")
@pytest.mark.parametrize('test_case_name', [
    '钱包-获取钱包列表'
])
def test_wallet_list_page(test_case_name, http_request):
    """
    测试获取钱包列表功能
    :return:
    """
    with allure.step("执行获取钱包列表测试"):
        result = wallet_list_page.get_wallet_list(test_case_name, http_request)
        assert_tools._common_response_validation_code(result, test_case_name)


@allure.epic("钱包模块")
@allure.feature("前置流程")
@pytest.mark.parametrize('test_case_name', [
    '钱包-获取支持的链列表'
])
@pytest.mark.priority("high")

def test_chain(test_case_name, http_request):
    """
    测试获取提现手续费
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :return:
    """
    result = wallet_list_page.get_chain_list(test_case_name, http_request)
    assert_tools._common_response_validation_code(result, test_case_name)




















@allure.epic("钱包模块")
@allure.feature("前置流程")
@pytest.mark.parametrize('test_case_name,currency_type', [
    ('获取设置法币和虚拟币种信息', 'fiat'),
    ('获取设置法币和虚拟币种信息', 'crypto')
])
@pytest.mark.priority("high")
def test_dropdown_crypto_fiat(test_case_name, http_request,currency_type):
    """
    测试获取支持的加密货币列表
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :return:
    """
    result = wallet_list_page.get_dropdown_for_currency_type(test_case_name, http_request,currency_type)
    assert_tools._common_response_validation_code(result, test_case_name)






# 定义货币类型常量
CURRENCY_TYPES = ['crypto', 'fiat']

# 获取配置数据并进行安全解析
def _get_config_data(currency_types):
    """获取并解析配置数据"""
    all_data_lists = []
    for currency_type in currency_types:
        value = config_tools.get_value(section=f'{currency_type}_data', key=f'{currency_type}_list')
        if value is not None and isinstance(value, str):
            try:
                data_lists = ast.literal_eval(value)
                if isinstance(data_lists, list):
                    all_data_lists.extend([(currency_type, item) for item in data_lists])
                else:
                    all_data_lists.extend([(currency_type, '')])  # 默认值处理
            except (ValueError, SyntaxError):
                # 配置解析失败时使用默认值
                all_data_lists.extend([(currency_type, '')])
        else:
            all_data_lists.extend([(currency_type, '')])
    return all_data_lists

# 预处理测试数据
PREPARED_TEST_DATA = _get_config_data(CURRENCY_TYPES)

@allure.epic("钱包模块")
@allure.feature("前置流程")
@pytest.mark.parametrize('test_case_name,currency_type,currency', [
    ('获取设置法币和虚拟币种信息', currency_type, currency)
    for currency_type, currency in PREPARED_TEST_DATA
])
def test_save_dropdown_for_currency_type(test_case_name, http_request, currency_type, currency):
    """
    测试获取并保存支持的货币类型下拉列表信息
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :param currency_type: 货币类型 (crypto/fiat)
    :param currency: 具体货币
    :return:
    """
    result = wallet_list_page.get_dropdown_for_currency_type(test_case_name, http_request, currency_type)
    wallet_list_page.save_dropdown_for_currency_type(result, currency_type, currency)






















@allure.epic("钱包模块")
@allure.feature("前置流程")
@pytest.mark.parametrize('test_case_name,transaction_type', [
    ('获取设置的payin/payout信息','crypto_payin'),
    ('获取设置的payin/payout信息','crypto_payout'),
])
@pytest.mark.priority("high")
def test_dropdown_for_transaction_type(test_case_name, http_request,transaction_type):
    """
    测试获取支持的加密货币列表
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :return:
    """
    result = wallet_list_page.get_dropdown_for_transaction_type(test_case_name, http_request,transaction_type)
    assert_tools._common_response_validation_code(result, test_case_name)









transaction_type = 'crypto_payin'
value = config_tools.get_value(section=f'{transaction_type}_data', key=f'{transaction_type}_dict')
if value is not None:
    country = ast.literal_eval(value)
else:
    country = []
test_transaction_type_and_country_case_name ='获取设置的payin/payout信息'
@allure.epic("钱包模块")
@allure.feature("前置流程")
@pytest.mark.parametrize("test_case_name, transaction_type, country", [
    (test_transaction_type_and_country_case_name, transaction_type, value)
    for key,value in country.items()
])
@pytest.mark.priority("high")
def test_dropdown_for_transaction_type_and_country_payin(test_case_name, http_request,transaction_type,country):
    """
    测试获取支持的加密货币列表
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :return:
    """
    result = wallet_list_page.get_dropdown_for_transaction_type_and_country(test_case_name, http_request,transaction_type,country)
    assert_tools._common_response_validation_code(result, test_case_name)






transaction_type = 'crypto_payout'
value = config_tools.get_value(section=f'{transaction_type}_data', key=f'{transaction_type}_dict')
if value is not None:
    country = ast.literal_eval(value)
else:
    country = []
test_transaction_type_and_country_case_name ='获取设置的payin/payout信息'
@allure.epic("钱包模块")
@allure.feature("前置流程")
@pytest.mark.parametrize("test_case_name, transaction_type, country", [
    (test_transaction_type_and_country_case_name, transaction_type, value)
    for key,value in country.items()
])
@pytest.mark.priority("high")
def test_dropdown_for_transaction_type_and_country_payout(test_case_name, http_request,transaction_type,country):
    """
    测试获取支持的加密货币列表
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :return:
    """
    result = wallet_list_page.get_dropdown_for_transaction_type_and_country(test_case_name, http_request,transaction_type,country)
    assert_tools._common_response_validation_code(result, test_case_name)






if __name__ == '__main__':
    pytest.main(['-s', 'test_wallet_list_page.py'])