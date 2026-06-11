import allure
import pytest
import ast
import traceback
from allure_commons.utils import format_traceback
import itertools
from api_processor.wallet_model import wallet_transaction
import Common.assert_tools as assert_tools
from Common.get_time import GetTime
import random

wallet_transaction = wallet_transaction.WalletTransaction()
assert_tools = assert_tools.AssertTools()





time = GetTime()
start_encoded, end_encoded = time.get_current_month_range()
currency = ['USDT','USDC']
to_transaction_type = ['crypto_payin',
                    'chain_deposit',
                    'checkout_withdraw',
                    'failed_refund',
                    'crypto_contract_out',
                    'card_account_to_wallet']

from_transaction_type = ['chain_withdraw',
                         'crypto_payout',
                         'crypto_contract_in',
                         'card_account_recharge',
                         'system_recharge',
                         'system_deduction']
transaction_status = ['completed','failed','pending']
test_case_name = '钱包-交易记录'

def generate_test_cases():
    test_cases = []

    # 组合 to_transaction_type 的情况
    for cur, trans_type, status in itertools.product(currency, to_transaction_type, transaction_status):
        test_cases.append((test_case_name, {
            'create_at': [start_encoded, end_encoded],
            'currency': cur,
            'transaction_type': trans_type,
            'transaction_status': status
        }))

    # 组合 from_transaction_type 的情况
    for cur, trans_type, status in itertools.product(currency, from_transaction_type, transaction_status):
        test_cases.append((test_case_name, {
            'create_at': [start_encoded, end_encoded],
            'currency': cur,
            'transaction_type': trans_type,
            'transaction_status': status
        }))

    return test_cases
@allure.epic("钱包模块")
@allure.feature("获取钱包交易数据")
@pytest.mark.parametrize(
    "test_case_name,body",generate_test_cases()

)
def test_get_wallet_transaction_data(test_case_name, http_request, body):
    """
    测试获取钱包交易数据
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :param body: 请求体参数
    """
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = wallet_transaction.get_transaction_data(http_request, test_case_name, body)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach()



@allure.epic("钱包模块")
@allure.feature("获取钱包交易列表")
def test_get_range_wallet_transaction_list(http_request,find_transaction_dict = {'process_status':'pending_approval'}):
    """
    测试获取钱包交易列表
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :param find_transaction_dict: 用于查找交易记录的字典，默认值为 {'process_status':'pending_approval'}
    """
    with allure.step(f"执行测试: 获取交易详情"):
        try:
            id_list = wallet_transaction.get_transaction_list_data(http_request, find_transaction_dict)
            transaction_id = random.choice(id_list)
            # print(transaction_id)
        except Exception as e:
            allure.attach(format_traceback(e.__traceback__), name="异常详情", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"测试失败: {e}")



@allure.epic("钱包模块")
@allure.feature("获取钱包交易详情")
@pytest.mark.parametrize(
    "test_case_name",
    [
        ('钱包-交易记录详情'),
    ]
)
def test_get_transaction_detail(http_request, test_case_name):
    """
    测试获取钱包交易详情
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    """
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            id_list = wallet_transaction.get_transaction_list_data(http_request, find_transaction_dict={'process_status': 'pending_approval'})
            if not id_list:
                pytest.fail("未找到符合条件的交易记录")
            transaction_id = random.choice(id_list)
            result = wallet_transaction.get_transaction_detail(http_request, test_case_name, transaction_id)
            assert_tools._common_response_validation_code(result, test_case_name)
        except IndexError:
            allure.attach(traceback.format_exc(), name="异常详情", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("未能选择有效的交易ID，请确认是否存在待审批状态的交易")
        except Exception as e:
            allure.attach(traceback.format_exc(), name="异常详情", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"测试失败: {e}")


@allure.epic("钱包模块")
@allure.feature("记录取消操作")
@pytest.mark.parametrize(
    "test_case_name",
    [
        ('钱包-取消交易'),
    ]
)
def test_cancel_transaction(http_request, test_case_name):
    """
    测试取消钱包交易
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    """
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            id_list = wallet_transaction.get_transaction_list_data(http_request, find_transaction_dict={'process_status': 'pending_approval'})
            if not id_list:
                pytest.fail("未找到符合条件的交易记录")
            transaction_id = random.choice(id_list)
            result = wallet_transaction.cancel_transaction(http_request, test_case_name, transaction_id)
            assert_tools._common_response_validation_code(result, test_case_name)
        except IndexError:
            allure.attach(traceback.format_exc(), name="异常详情", attachment_type=allure.attachment_type.TEXT)
            pytest.fail("未能选择有效的交易ID，请确认是否存在待审批状态的交易")
        except Exception as e:
            allure.attach(traceback.format_exc(), name="异常详情", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"测试失败: {e}")