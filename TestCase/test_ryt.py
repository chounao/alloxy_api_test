# -*- coding: utf-8 -*-
import allure
import pytest
from api_processor.RYT_model import RYT
import Common.assert_tools as assert_tools


assert_tools = assert_tools.AssertTools()
ryt = RYT.Ryt()

test_get_account_info_case_name = '获取用户ryt信息'
@allure.epic("RYT")
@allure.feature("RYT模块")
@allure.story("获取账户信息")
def test_get_account_info(http_request):
    with allure.step(f"执行测试: {test_get_account_info_case_name}"):
        result = ryt.get_account_info(http_request, test_get_account_info_case_name)
        assert_tools._common_response_validation_code(result, test_get_account_info_case_name)




test_get_supply_info_case_name = '获取供应量信息'
@allure.epic("RYT")
@allure.feature("RYT模块")
@allure.story("获取供应量信息")
def test_get_supply_info(http_request):
    with allure.step(f"执行测试: {test_get_supply_info_case_name}"):
        result = ryt.get_supply_info(http_request, test_get_supply_info_case_name)
        assert_tools._common_response_validation_code(result, test_get_supply_info_case_name)





test_get_price_list_info_case_name = '获取价格列表信息'
@allure.epic("RYT")
@allure.feature("RYT模块")
@allure.story("获取价格列表信息")
def test_get_price_list_info(http_request):
    with allure.step(f"执行测试: {test_get_price_list_info_case_name}"):
        result = ryt.get_price_list_info(http_request, test_get_price_list_info_case_name)
        assert_tools._common_response_validation_code(result, test_get_price_list_info_case_name)




test_get_profit_list_info_case_name = '获取利润清单信息'
@allure.epic("RYT")
@allure.feature("RYT模块")
@allure.story("获取利润清单信息")
def test_get_profit_list_info(http_request):
    with allure.step(f"执行测试: {test_get_profit_list_info_case_name}"):
        result = ryt.get_profit_list_info(http_request, test_get_profit_list_info_case_name)
        assert_tools._common_response_validation_code(result, test_get_profit_list_info_case_name)





test_get_transaction_data_case_name = '获取交易记录'
@allure.epic("RYT")
@allure.feature("RYT模块")
@allure.story("获取交易记录")
def test_get_transaction_data(http_request):
    with allure.step(f"执行测试: {test_get_transaction_data_case_name}"):
        result = ryt.get_transaction_record(http_request, test_get_transaction_data_case_name)
        assert_tools._common_response_validation_code(result, test_get_transaction_data_case_name)



test_buy_ryt_case_name = 'RYT购入'
@allure.epic("RYT")
@allure.feature("RYT模块")
@allure.story("RYT购入")
@pytest.mark.parametrize(
    'test_case_name,amount',
    [
        (test_buy_ryt_case_name, '100'),
        (test_buy_ryt_case_name, '1000'),
        (test_buy_ryt_case_name, '10000'),
        (test_buy_ryt_case_name, '100000'),
        (test_buy_ryt_case_name, '1000000'),
        (test_buy_ryt_case_name, '10000000'),
    ]
)
def test_buy_ryt(http_request, test_case_name, amount):
    with allure.step(f"执行测试: {test_buy_ryt_case_name}"):
        result = ryt.buy_ryt(http_request, test_case_name, amount)
        assert_tools._common_response_validation_code(result, test_buy_ryt_case_name)





test_sell_ryt_case_name = 'RYT赎回'
@allure.epic("RYT")
@allure.feature("RYT模块")
@allure.story("RYT赎回")
@pytest.mark.parametrize(
    'test_case_name,amount',
    [
        (test_sell_ryt_case_name, '0.0001')
    ]
)
def test_sell_ryt(http_request, test_case_name, amount):
    with allure.step(f"执行测试: {test_sell_ryt_case_name}"):
        result = ryt.sell_ryt(http_request, test_case_name, amount)
        assert_tools._common_response_validation_code(result, test_sell_ryt_case_name)


if __name__ == '__main__':
    pytest.main(['-s', 'test_ryt.py'])