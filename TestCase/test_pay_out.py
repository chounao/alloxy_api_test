# -*- coding: utf-8 -*-
import allure
import pytest
import random
from api_processor.wallet_model import pay_out
from api_processor.wallet_model.wallet_list_page import WalletListPage
import Common.assert_tools as assert_tools
from Common.read_and_save_tool import ConfigTools
from typing import List, Optional

config = ConfigTools()

pay_out_instance = pay_out.PayOut()
wallet_list_page = WalletListPage()

CURRENCY_LIST = ['USDT', 'USDC']
MEMO_LIST = ['gift', 'bills', 'groceries', 'travel', 'health', 'entertainment', 'housing', 'school-fees', 'other']

PAYOUT_TYPE = 'payout'
CURRENCY_KEY = 'currency'
MIN_LIMIT_KEY = 'min_limit'

def get_params(case_name: str,
               type_: str,
               key_name: Optional[List[str]] = None,
               include_amount: bool = False,
               include_from_currency: bool = False,
               include_to_currency: bool = False,
               include_memo: bool = False) -> List[tuple]:
    """
    获取测试参数列表

    Args:
        case_name: 测试用例名称
        type_: 数据类型
        key_name: 键名列表
        include_amount: 是否包含金额参数
        include_from_currency: 是否包含源加密货币参数
        include_to_currency: 是否包含目标加密货币参数
        include_memo: 是否包含备注参数

    Returns:
        list: 测试参数列表
    """
    test_params_list = []

    try:
        values = config.get_yellow_card_data(type_, key_name or [])
    except KeyError as e:
        print(f"Missing configuration key: {e}")
        return test_params_list
    except Exception as e:
        print(f"Unexpected error fetching data from config: {e}")
        return test_params_list

    if not values:
        return test_params_list

    for from_currency in CURRENCY_LIST:
        for value in values:
            # 完整组合：amount + memo + from_currency + to_currency
            if include_amount and include_memo and include_from_currency and include_to_currency and len(value) >= 2:
                to_currency = value[0]
                amount = value[1]
                memo = random.choice(MEMO_LIST)
                test_params_list.append((case_name, from_currency, to_currency, amount, memo))

            # 只含 from_currency 和 to_currency
            elif include_from_currency and include_to_currency and len(value) == 1:
                to_currency = value[0]
                test_params_list.append((case_name, from_currency, to_currency))

            # 仅含 to_currency
            elif include_to_currency and len(value) == 1:
                to_currency = value[0]
                test_params_list.append((case_name, to_currency))

    return test_params_list


test_get_fiat_fee_case_name = '获取加密货币到法币手续费'


@allure.epic("钱包模块")
@allure.feature("pay_out流程")
@pytest.mark.parametrize('test_case_name', [(test_get_fiat_fee_case_name)])
@pytest.mark.priority("high")
def test_get_fiat_fee(http_request, test_case_name):
    """
    测试获取加密货币到法币手续费
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :return:
    """
    with allure.step(f"执行测试: {test_case_name}"):
        result = pay_out_instance.get_fiat_fee_info(http_request, test_case_name)
        assert_tools.AssertTools()._common_response_validation_code(result, test_case_name)







@pytest.mark.priority("high")
def test_fiat_rate(http_request, test_case_name, from_currency, to_currency):
    """
    测试获取pay_out汇率
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :param from_currency: 加密货币
    :param to_currency:
    :return:
    """
    with allure.step(f"执行测试: {test_case_name}"):
        result = pay_out_instance.get_fiat_rate_info(http_request, test_case_name, from_currency, to_currency)
        assert_tools.AssertTools()._common_response_validation_code(result, test_case_name)


test_payee_case_name = '钱包-获取法币收款地址列表'


@allure.epic("钱包模块")
@allure.feature("pay_out流程")
@pytest.mark.parametrize('test_case_name,to_currency',
                         get_params(
                             test_payee_case_name,
                             PAYOUT_TYPE,
                             [CURRENCY_KEY],
                             include_to_currency=True))
def test_payee_info(http_request, test_case_name, to_currency):
    """
    测试获取法币收款地址列表
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :param currency: 法币
    :return:
    """
    with allure.step(f"执行测试: {test_case_name}"):
        result = pay_out_instance.get_payee_info(http_request, test_case_name, to_currency)
        assert_tools.AssertTools()._common_response_validation_code(result, test_case_name)



test_get_config_setting_name = '获取设置的payin/payout信息'


@allure.epic("钱包模块")
@allure.feature("pay_out流程")
@pytest.mark.parametrize(
    'test_case_name',
    get_params(
        test_get_config_setting_name,
        PAYOUT_TYPE,
        [CURRENCY_KEY],
        include_to_currency=True
    )
)
def test_get_config_setting(http_request, test_case_name, to_currency):
    """
    测试获取pay_out汇率
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :param from_currency: 加密货币
    :param to_currency: 法币
    :return:
    """
    with allure.step(f"执行测试: {test_case_name}"):
        result = pay_out_instance.get_config_setting_for_limit(http_request,test_case_name,to_currency)
        assert_tools.AssertTools()._common_response_validation_code(result, test_case_name)
def test_setting(http_request):
    result = pay_out_instance.get_config_setting_for_limit(http_request, '获取设置的payin/payout信息', 'RWF')
    print( result)




def test_pay_out_parameter(http_request, from_currency='USDT', to_currency='BWP', amount=160, memo='gift'):
    """
    测试法币转出参数
    :param http_request: HttpRequest实例
    :param from_currency: 加密货币
    :param to_currency: 法币
    :param amount: 金额
    :param memo: 备注
    :return:
    """
    result = pay_out_instance.pay_out_parameter(http_request, from_currency, to_currency, amount, memo)
    print(result)



test_pay_out_case_name = 'pay_out操作'

@allure.epic("钱包模块")
@allure.feature("pay_out流程")
@pytest.mark.parametrize(
    'test_case_name,from_currency,to_currency,amount,memo',
    get_params(
        test_pay_out_case_name,
        PAYOUT_TYPE,
        [CURRENCY_KEY, MIN_LIMIT_KEY],
        include_from_currency=True,
        include_to_currency=True,
        include_memo=True,
        include_amount=True
    )
)
def test_pay_out(http_request, test_case_name, from_currency, to_currency, amount, memo, before_wallet_data_out_type):
    """
    测试法币转出
    :param test_case_name: 测试用例名称
    :param http_request: HttpRequest实例
    :param from_currency: 加密货币
    :param to_currency: 法币
    :param amount: 金额
    :param memo: 备注
    :return:
    """
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            variables = pay_out_instance.pay_out_parameter(http_request, from_currency, to_currency, amount, memo)
            result = pay_out_instance.create_pay_out(variables, http_request, test_case_name, from_currency, to_currency,
                                                     amount, memo)
            assert_tools.AssertTools()._common_response_validation_code(result, test_case_name)

            # 断言业务逻辑，转账后币种余额是否正确

            price_data = before_wallet_data_out_type.get('price',0)
            after_amount = wallet_list_page.get_currency_data(http_request, from_currency)
            fee = pay_out_instance.pay_out_fee(http_request,from_currency,to_currency, amount)
            assert_tools.AssertTools()._common_response_validation_amount(
                currency= after_amount,
                before_amount= before_wallet_data_out_type,
                after_amount= after_amount,
                amount= amount,
                fee= fee,
                test_case_name= test_case_name,
                with_fee=True)
        except AssertionError as ae:
            allure.attach(f"断言失败: {str(ae)}", name="断言信息")
            raise
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise

@allure.epic("钱包模块")
@allure.feature("pay_out流程")
@pytest.mark.parametrize("from_currency,to_currency,amount", [
    ("USDT", "UGX", 100)
])
def test_pay_out_fee(http_request,from_currency,to_currency, amount):
    """
    测试法币转出手续费
    :param http_request: HttpRequest实例
    :param from_currency: 加密货币
    :param to_currency: 法币
    :param amount: 金额
    :return:
    """
    with allure.step(f"执行测试: 计算所有手续费包括网络清算的手续费"):
        fee = pay_out_instance.pay_out_fee(http_request,from_currency, to_currency, amount)
        print(fee)


def test_get_rate_data(http_request):
    """
    测试获取法币转出的汇率数据
    :param http_request: HttpRequest实例
    :param to_currency: 法币
    :param id: 支付渠道id
    :return:
    """
    with allure.step(f"执行测试: 获取法币转出的汇率数据"):
        result = pay_out_instance.get_country_rate_data(http_request,from_currency='USDT',id = 'af1e6168-9966-4569-b2f7-d298fd680a37')
        print(result)
if __name__ == '__main__':
    pytest.main(['-s', 'test_pay_out.py'])
