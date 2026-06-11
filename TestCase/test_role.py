# -*- coding: utf-8 -*-
import allure
import pytest
from api_processor.management_model import role
import Common.assert_tools as assert_tools

role = role.RoleManagement()
assert_tools = assert_tools.AssertTools()


test_create_role_case_name = '管理-创建角色'
@allure.epic('管理模块')
@allure.feature('角色管理')
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_create_role_case_name])
def test_create_role(test_case_name, http_request):
    with allure.step(f'执行测试: {test_case_name}'):
        try:
            result = role.create_role(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise


def test_get_id(http_request):
    id_data = role.get_role_id(http_request)
    print(id_data)


test_get_role_data_case_name = '管理-获取角色列表'
@allure.epic('管理模块')
@allure.feature('角色管理')
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_get_role_data_case_name])
def test_get_role_data(test_case_name, http_request):
    with allure.step(f'执行测试: {test_case_name}'):
        try:
            result = role.get_role_data(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise



test_put_role_case_name = '管理-更新角色'
@allure.epic('管理模块')
@allure.feature('角色管理')
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_put_role_case_name])
def test_put_role(test_case_name, http_request):
    with allure.step(f'执行测试: {test_case_name}'):
        try:
            result = role.put_role(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise





tets_delete_role_case_name = '管理-删除角色'
@allure.epic("管理页面")
@allure.feature("角色管理")
@pytest.mark.priority("high")
@pytest.mark.parametrize('test_case_name', [tets_delete_role_case_name])
def test_delete_role(test_case_name, http_request):
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = role.get_role_data(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise
