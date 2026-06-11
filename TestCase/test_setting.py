# -*- coding: utf-8 -*-
import allure
import pytest
from api_processor.management_model import setting
import Common.assert_tools as assert_tools


setting = setting.Settings()
assert_tools = assert_tools.AssertTools()
model_name = '风控设置'
Set_function_name =['审批设置','风控策略设置','白名单','黑名单']



test_get_trx_review_settings_case_name = '管理-获取审批设置列表'
@allure.epic(model_name)
@allure.feature(Set_function_name[0])
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_get_trx_review_settings_case_name])
def test_get_trx_review_settings(test_case_name,http_request):
    with allure.step(f'执行测试{test_case_name}'):
        try:
            result = setting.get_trx_review_settings(http_request,test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise


test_create_trx_review_settings_case_name = '管理-创建审批设置'
@allure.epic(model_name)
@allure.feature(Set_function_name[0])
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_create_trx_review_settings_case_name])
def test_create_trx_review_settings(test_case_name,http_request):
    with allure.step(f'执行测试{test_case_name}'):
        try:
            result = setting.create_trx_review_settings(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise



test_update_trx_review_settings_name = '管理-修改审批设置'
@allure.epic(model_name)
@allure.feature(Set_function_name[0])
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_update_trx_review_settings_name])
def test_update_trx_review_settings(test_case_name,http_request):
    with allure.step(f'执行测试{test_case_name}'):
        try:
            result = setting.update_trx_review_settings(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise




test_delect_trx_review_settings_name = '管理-删除审批设置'
@allure.epic(model_name)
@allure.feature(Set_function_name[0])
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_delect_trx_review_settings_name])
def test_delect_trx_review_settings(test_case_name,http_request):
    with allure.step(f'执行测试{test_case_name}'):
        try:
            result = setting.delete_trx_review_settings(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise





test_get_risk_policy_settings_case_name = '管理-查询风控设置'
@allure.epic(model_name)
@allure.feature(Set_function_name[1])
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_get_risk_policy_settings_case_name])
def test_get_risk_policy_settings(test_case_name,http_request):
    with allure.step(f'执行测试{test_case_name}'):
        try:
            result = setting.get_risk_policy_settings(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise


def test_find_create_risk_policy_settings_data(http_request):
    setting.find_create_risk_policy_settings_data(http_request)

"""

=================
"""

test_create_risk_policy_settings_case_name = '管理-创建风控设置'
@allure.epic(model_name)
@allure.feature(Set_function_name[1])
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_create_risk_policy_settings_case_name])
def test_get_risk_policy_settings(test_case_name,http_request):
    with allure.step(f'执行测试{test_case_name}'):
        try:
            result = setting.create_risk_policy_settings(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise




test_delete_risk_policy_settings_case_name = '管理-删除风控设置'
@allure.epic(model_name)
@allure.feature(Set_function_name[1])
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_delete_risk_policy_settings_case_name])
def test_get_risk_policy_settings(test_case_name,http_request):
    with allure.step(f'执行测试{test_case_name}'):
        try:
            result = setting.delete_risk_policy_settings(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise






test_delete_risk_policy_settings_case_name = '管理-查询白名单列表'
@allure.epic(model_name)
@allure.feature(Set_function_name[2])
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_delete_risk_policy_settings_case_name])
def test_get_risk_policy_settings(test_case_name,http_request):
    with allure.step(f'执行测试{test_case_name}'):
        try:
            result = setting.delete_risk_policy_settings(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise



TEST_WHIITE_DATA = [
        {"business_type":"bank_no",
         "no_address":"0x175aa0ecbe43e52bd002a30d65ede10b16c75408",
         "day_limit":1,
         "single_limit":10,
         "total_limit":20,
         "name_type":"white"},
        {"business_type": "crypto_address",
         "no_address": "0x175aa0ecbe43e52bd002a30d65ede10b16c75408",
         "day_limit": 1,
         "single_limit": 10,
         "total_limit": 20,
         "name_type": "white"}
]
test_create_trx_namelist_white_list_case_name = '管理-创建白名单列表'
@allure.epic(model_name)
@allure.feature(Set_function_name[3])
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name,payload', [
    (test_create_trx_namelist_white_list_case_name, TEST_WHIITE_DATA[0]),
    (test_create_trx_namelist_white_list_case_name, TEST_WHIITE_DATA[1])
])
def test_create_trx_namelist_white_list(test_case_name, payload, http_request):
    with allure.step(f'执行测试{test_case_name}'):
        try:
            result = setting.create_trx_namelist_white_list(http_request, test_case_name, payload)
            assert_tools._common_response_validation_code(result, test_case_name)
        except AssertionError as e:
            allure.attach(f'断言失败：{str(e)}', name='断言信息')
            raise
        except Exception as e:
            allure.attach(f'测试执行异常：{str(e)}', name='异常信息')
            raise

test_get_trx_namelist_white_log_case_name = '管理-查看白名单日志'
@allure.epic(model_name)
@allure.feature(Set_function_name[3])
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_get_trx_namelist_white_log_case_name])
def test_get_trx_namelist_white_logs(test_case_name,http_request):
    with allure.step(f'执行测试{test_case_name}'):
        try:
            result = setting.get_trx_namelist_write_log(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise

test_delete_trx_namelist_white_list_case_name = '管理-删除白名单'
@allure.epic(model_name)
@allure.feature(Set_function_name[3])
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_delete_trx_namelist_white_list_case_name])
def test_delete_trx_namelist_white_list(test_case_name,http_request):
    with allure.step(f'执行测试{test_case_name}'):
        try:
            result = setting.delete_trx_namelist_white_list(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')









test_get_trx_namelist_black_list_case_name = '管理-查询黑名单列表'
@allure.epic(model_name)
@allure.feature(Set_function_name[3])
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_get_trx_namelist_black_list_case_name])
def test_get_risk_policy_settings(test_case_name,http_request):
    with allure.step(f'执行测试{test_case_name}'):
        try:
            result = setting.get_trx_namelist_black_list(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise



def test_find_trx_namelist_black_list_data(http_request):
    setting.find_get_trx_namelist_black_list_data(http_request)





TEST_BLACKLIST_DATA = [
    {
        "business_type": "bank_no",
        "name_type": "black",
        "no_address": "0x175aa0ecbe43e52bd002a30d65ede10b16c75408"
    },
    {
        "business_type": "crypto_address",
        "name_type": "black",
        "no_address": "0x175aa0ecbe43e52bd002a30d65ede10b16c75409"
    }
]

test_create_trx_namelist_black_list_case_name = '管理-创建黑名单列表'
@allure.epic(model_name)
@allure.feature(Set_function_name[3])
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name,payload', [
    (test_create_trx_namelist_black_list_case_name, TEST_BLACKLIST_DATA[0]),
    (test_create_trx_namelist_black_list_case_name, TEST_BLACKLIST_DATA[1])
])
def test_create_trx_namelist_black_list(test_case_name, payload, http_request):
    with allure.step(f'执行测试{test_case_name}'):
        try:
            result = setting.create_trx_namelist_black_list(http_request, test_case_name, payload)
            assert_tools._common_response_validation_code(result, test_case_name)
        except AssertionError as e:
            allure.attach(f'断言失败：{str(e)}', name='断言信息')
            raise
        except Exception as e:
            allure.attach(f'测试执行异常：{str(e)}', name='异常信息')
            raise

test_get_trx_namelist_black_log_case_name = '管理-查看黑名单日志'
@allure.epic(model_name)
@allure.feature(Set_function_name[3])
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_get_trx_namelist_black_log_case_name])
def test_get_trx_namelist_black_logs(test_case_name,http_request):
    with allure.step(f'执行测试{test_case_name}'):
        try:
            result = setting.get_trx_namelist_black_log(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise

test_delete_trx_namelist_black_list_case_name = '管理-删除黑名单'
@allure.epic(model_name)
@allure.feature(Set_function_name[3])
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_delete_trx_namelist_black_list_case_name])
def test_delete_trx_namelist_black_list(test_case_name,http_request):
    with allure.step(f'执行测试{test_case_name}'):
        try:
            result = setting.delete_trx_namelist_black_list(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')