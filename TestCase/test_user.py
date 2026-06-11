# -*- coding: utf-8 -*-
import allure
import pytest

from TestCase.test_role import test_create_role
from api_processor.management_model import user
import Common.assert_tools as assert_tools

import ast
user = user.UserManagement ()
assert_tools = assert_tools.AssertTools()


def test_get_id(http_request):
    id = user.get_id_for_name(http_request)
    return id

test_create_user_case_name = '管理-创建成员'
@allure.epic('管理模块')
@allure.feature('用户管理')
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_create_user_case_name])
def test_create_user(test_case_name, http_request):
 with allure.step(f'执行测试: {test_case_name}'):
     try:
         result = user.create_user(http_request, test_case_name)
         assert_tools._common_response_validation_code(result, test_case_name)
     except Exception as e:
         allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
         raise





test_get_user_id_case_name = '管理-获取成员列表'
@allure.epic('管理模块')
@allure.feature('用户管理')
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_get_user_id_case_name])
def test_get_user_id(test_case_name, http_request):
    with allure.step(f'执行测试: {test_case_name}'):
        try:
            result = user.get_user_id(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise






test_resat_password_case_name = '管理-重置成员密码'
@allure.epic('管理模块')
@allure.feature('用户管理')
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_resat_password_case_name])
def test_resat_password(test_case_name, http_request):
    with allure.step(f'执行测试: {test_case_name}'):
        try:
            result = user.reset_password(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise






test_update_case_name = '管理-更新成员'
@allure.epic('管理模块')
@allure.feature('用户管理')
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_update_case_name])
def test_update_user(test_case_name, http_request):
    with allure.step(f'执行测试: {test_case_name}'):
        try:
            result = user.update_user_info(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise









test_delect_user_case_name = '管理-删除成员'
@allure.epic('管理模块')
@allure.feature('用户管理')
@pytest.mark.priority('high')
@pytest.mark.parametrize('test_case_name', [test_delect_user_case_name])
def test_delect_user(test_case_name, http_request):
    with allure.step(f'执行测试: {test_case_name}'):
        try:
            result = user.delete_user(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f'测试执行异常: {str(e)}', name='异常信息')
            raise


