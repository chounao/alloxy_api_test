# -*- coding: utf-8 -*-
import allure
import pytest
from api_processor.business_card import Card_account_Management
import Common.assert_tools as assert_tools


card_account_management = Card_account_Management.CardAccountManagement
assert_tools = assert_tools.AssertTools()

# balance_type = 'cardAccountBalance'
balance_type = 'cardBalance'
test_get_card_balance_case_name = '获取卡账户余额和卡余额'
@allure.epic("数字商务卡")
@allure.feature("卡管理页面")
@pytest.mark.priority("high")
@pytest.mark.parametrize('test_case_name,balance_type', [(test_get_card_balance_case_name,balance_type)])
def test_get_card_balance(test_case_name, http_request,balance_type):
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = card_account_management.get_cardAccountBalance_and_cardBalance(http_request, test_case_name,balance_type)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise




test_card_account_recharge_params_case_name = '卡账户充值参数'
@allure.epic("数字商务卡")
@allure.feature("卡管理页面")
@allure.story("卡账户充值参数")
@pytest.mark.priority("high")
@pytest.mark.parametrize('from_currency,amount', [('USDT',100)])
def test_card_account_recharge_params(http_request,from_currency, amount,before_wallet_data_out_type):
    with allure.step(f"执行测试: {test_card_account_recharge_params_case_name}"):
        before_wallet = before_wallet_data_out_type.get('id',0)
        print(f"before_wallet:{before_wallet}")

        result = card_account_management.card_account_recharge_params(before_wallet,from_currency, amount)
