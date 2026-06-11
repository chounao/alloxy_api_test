# -*- coding: utf-8 -*-
import allure
import pytest
from api_processor.business_card import card_transction
import Common.assert_tools as assert_tools

transaction = card_transction.CardTransaction()
assert_tools = assert_tools.AssertTools()


card_transaction_type = ['card_consume','card_clearing','card_reversal','card_refund','card_deposit','card_to_card_account','card_clearing_deduction','card_clearing_refund','card_transaction_authorization_fee','card_atm','card_declined_refund']
card_status = ['pending','completed','failed']
test_card_transaction_case_name = '获取交易记录'
# params_body = ['card_consume','pending','card']

def get_params_body(transaction_sub_type,transaction_type):
    params_body = []
    for transaction_types in transaction_type:
        for status in card_status:
            params_body.append([transaction_types, status, transaction_sub_type])
    return params_body


@allure.epic("数字商务卡")
@allure.feature("交易记录页面")
@pytest.mark.priority("high")
@pytest.mark.parametrize(
    'test_case_name,transaction_type,status,transaction_sub_type',
    [(test_card_transaction_case_name, t_type, status, sub_type)
     for t_type, status, sub_type in get_params_body('card', card_transaction_type)]
)
def test_get_card_transaction(test_case_name, http_request, transaction_type,status,transaction_sub_type):
    with allure.step(f"执行测试：{test_case_name}"):
        try:
            result = transaction.get_card_transaction_data(
                http_request,
                test_case_name,
                transaction_type,status,transaction_sub_type

            )
            assert_tools._common_response_validation_code(result, test_case_name)

            # 添加对返回数据的基本验证
            assert result is not None, "返回结果不能为空"
            if isinstance(result, dict):
                assert 'data' in result or 'code' in result, "返回结果格式不正确"

        except AssertionError as e:
            allure.attach(f"断言失败：{str(e)}", name="断言失败信息")
            raise
        except Exception as e:
            import traceback
            error_details = f"测试执行异常：{str(e)}\n堆栈信息:\n{traceback.format_exc()}"
            allure.attach(error_details, name="异常详细信息")
            raise





card_account_transaction_type =['vcc_in','vcc_out','card_transaction_authorization_fee','system_deduction','system_recharge','card_holder_kyc_fee_out','card_holder_kyc_fee_refund','logistics_fee','card_create_virtual','card_create_physical']

@allure.epic("数字商务卡")
@allure.feature("交易记录页面")
@pytest.mark.priority("high")
@pytest.mark.parametrize(
    'test_case_name,transaction_type,status,transaction_sub_type',
    [(test_card_transaction_case_name, t_type, status, sub_type)
     for t_type, status, sub_type in get_params_body('card_account',card_account_transaction_type)]
)
def test_get_card_account_transaction(test_case_name, http_request, transaction_type,status,transaction_sub_type):
    with allure.step(f"执行测试：{test_case_name}"):
        try:
            result = transaction.get_card_transaction_data(
                http_request,
                test_case_name,
                transaction_type,status,transaction_sub_type

            )
            assert_tools._common_response_validation_code(result, test_case_name)

            # 添加对返回数据的基本验证
            assert result is not None, "返回结果不能为空"
            if isinstance(result, dict):
                assert 'data' in result or 'code' in result, "返回结果格式不正确"

        except AssertionError as e:
            allure.attach(f"断言失败：{str(e)}", name="断言失败信息")
            raise
        except Exception as e:
            import traceback
            error_details = f"测试执行异常：{str(e)}\n堆栈信息:\n{traceback.format_exc()}"
            allure.attach(error_details, name="异常详细信息")
            raise

if __name__ == '__main__':
    pytest.main(['-s', 'test_card_transaction.py'])