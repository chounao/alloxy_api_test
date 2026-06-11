# -*- coding: utf-8 -*-
import allure
import pytest
import Common.assert_tools as assert_tools
from api_processor.home_model.home_page import HomePage

home = HomePage()
assert_tools = assert_tools.AssertTools()

@allure.epic("首页功能")
@allure.feature("用户首页")
@pytest.mark.parametrize('test_case_name', ['用户信息'])
@pytest.mark.priority("high")
def test_user_data(test_case_name,http_request):
    """
    获取登录数据
    :param test_case_name: 测试用例名称
    """
    with allure.step(f"执行首页测试: {test_case_name}"):
        result = home.get_user_data(test_case_name,http_request)
        assert_tools._common_response_validation_code(result, test_case_name)

@allure.epic("首页功能")
@allure.feature("用户首页")
@pytest.mark.parametrize('test_case_name', ['获取权限状态'])
@pytest.mark.priority("high")
def test_user_menu_permission(test_case_name,http_request):
    """
    获取用户菜单权限
    :param test_case_name: 测试用例名称
    """
    with allure.step(f"执行首页测试: {test_case_name}"):
        result = home.get_user_menus(test_case_name,http_request)  # 修正方法名
        assert_tools._common_response_validation_code(result, test_case_name)




@allure.epic("首页功能")
@allure.feature("用户首页")
@pytest.mark.parametrize('test_case_name', ['账号信息统计'])
@pytest.mark.priority("high")
def test_user_account_overview(test_case_name,http_request):
    """
    获取账号信息统计
    :param test_case_name: 测试用例名称
    :param dict_key: 字典键名，默认值为'transaction_list'
    """
    with allure.step(f"执行首页测试: {test_case_name}"):
        result = home.get_user_account_overview(test_case_name,http_request,dict_key='transaction_list',list_key ='id')  # 修正方法名
        assert_tools._common_response_validation_code(result, test_case_name)


@allure.epic("首页功能")
@allure.feature("用户首页")
@pytest.mark.parametrize('test_case_name', ['获取代办列表'])
@pytest.mark.priority("high")
def test_get_todo_data(test_case_name,http_request):
    """
    获取账号信息统计
    :param test_case_name: 测试用例名称
    """
    with allure.step(f"执行首页测试: {test_case_name}"):
        result = home.get_todo_data(test_case_name,http_request)  # 修正方法名
        assert_tools._common_response_validation_code(result, test_case_name)



@allure.epic("首页功能")
@allure.feature("用户首页")
@pytest.mark.parametrize('test_case_name', ['获取消息通知列表'])
@pytest.mark.priority("high")
def test_get_notices(test_case_name,http_request):
    """
    获取账号信息统计
    :param test_case_name: 测试用例名称
    """
    with allure.step(f"执行首页测试: {test_case_name}"):
        result = home.get_notices(test_case_name,http_request)  # 修正方法名
        assert_tools._common_response_validation_code(result, test_case_name)



@allure.epic("首页功能")
@allure.feature("用户首页")
@pytest.mark.parametrize('test_case_name', ['交易详情_PASS'])
@pytest.mark.priority("high")
def test_get_transacton_detail_PASS(test_case_name,http_request):
    """
    获取账号信息统计
    :param test_case_name: 测试用例名称
    """
    with allure.step(f"执行首页测试: {test_case_name}"):
        transaction_id = home._get_transaction_id(http_request)
        result = home.get_transacton_detail(test_case_name,http_request,{"id": transaction_id} )  # 修正方法名
        assert_tools._common_response_validation_code(result, test_case_name)



@allure.epic("首页功能")
@allure.feature("用户首页")
@pytest.mark.parametrize('test_case_name', ['交易详情_ID_NULL'])
@pytest.mark.priority("high")
def test_get_transacton_detail_fail01(test_case_name,http_request):
    """
    获取账号信息统计
    :param test_case_name: 测试用例名称
    """
    with allure.step(f"执行首页测试: {test_case_name}"):
        result = home.get_transacton_detail(test_case_name,http_request,{"id": "NULL"})
        assert_tools._common_response_validation_code(result, test_case_name)



@allure.epic("首页功能")
@allure.feature("用户首页")
@pytest.mark.parametrize('test_case_name', ['交易详情_ID_ERROR'])
@pytest.mark.priority("high")
def test_get_transacton_detail_fail02(test_case_name,http_request):
    """
    获取账号信息统计
    :param test_case_name: 测试用例名称
    """
    with allure.step(f"执行首页测试: {test_case_name}"):
        result = home.get_transacton_detail(test_case_name,http_request,{"id": -1})
        assert_tools._common_response_validation_code(result, test_case_name)



@allure.epic("首页功能")
@allure.feature("用户首页")
@pytest.mark.parametrize('test_case_name', ['交易详情_NOT_UUID'])
@pytest.mark.priority("high")
def test_get_transacton_detail_fail03(test_case_name,http_request):
    """
    获取账号信息统计
    :param test_case_name: 测试用例名称
    """
    with allure.step(f"执行首页测试: {test_case_name}"):
        result = home.get_transacton_detail(test_case_name,http_request,{"id": "185380497799"})
        assert_tools._common_response_validation_code(result, test_case_name)



@allure.epic("首页功能")
@allure.feature("用户首页")
@pytest.mark.parametrize('test_case_name', ['交易详情_PUT_SQL'])
@pytest.mark.priority("high")
def test_get_transacton_detail_fail04(test_case_name,http_request):
    """
    获取账号信息统计
    :param test_case_name: 测试用例名称
    """
    with allure.step(f"执行首页测试: {test_case_name}"):
        result = home.get_transacton_detail(test_case_name,http_request,{"id": "1' OR 1=1--"})
        assert_tools._common_response_validation_code(result, test_case_name)



@allure.epic("首页功能")
@allure.feature("用户首页")
@pytest.mark.parametrize('test_case_name', ['交易详情_PUT_XSS'])
@pytest.mark.priority("high")
def test_get_transacton_detail_fail05(test_case_name,http_request):
    """
    获取账号信息统计
    :param test_case_name: 测试用例名称
    """
    with allure.step(f"执行首页测试: {test_case_name}"):
        result = home.get_transacton_detail(test_case_name,http_request,{"id": '<script>alert(1)</script>'})
        assert_tools._common_response_validation_code(result, test_case_name)




if __name__ == '__main__':
    pytest.main(["-s", "--env", "test", "--priority", "high", "--collect-only",
                 "/Users/alloyx/Desktop/alloxy_api_testcase_framework/TestCase/test_home.py"])