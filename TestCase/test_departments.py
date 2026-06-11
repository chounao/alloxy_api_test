# -*- coding: utf-8 -*-
import allure
import pytest
import Common.assert_tools as assert_tools
from TestCase.test_card_holders import test_get_department_id
from api_processor.management_model import department
from Common.read_and_save_tool import ConfigTools
import ast


departments = department.Departments()
assert_tools = assert_tools.AssertTools()
config_tools = ConfigTools()


test_get_department_data_case_name = '管理-获取部门列表'
@allure.epic("管理页面")
@allure.feature("组织架构")
@pytest.mark.priority("high")
@pytest.mark.parametrize('test_case_name', [test_get_department_data_case_name])

def test_get_department_data(test_case_name, http_request):

    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = departments.get_department_data(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise








test_create_department_case_name = '管理-创建部门'
@allure.epic("管理页面")
@allure.feature("组织架构")
@pytest.mark.priority("high")
@pytest.mark.parametrize('test_case_name', [test_create_department_case_name])
def test_create_department(test_case_name, http_request):
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = departments.create_department(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise








test_put_department_case_name = '管理-更新部门'
@allure.epic("管理页面")
@allure.feature("组织架构")
@pytest.mark.priority("high")
@pytest.mark.parametrize('test_case_name', [test_create_department_case_name])
def test_put_department(test_case_name, http_request):
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = departments.put_department(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise





test_delect_department_case_name = "管理-删除部门"
@allure.epic("管理页面")
@allure.feature("组织架构")
@pytest.mark.priority("high")
@pytest.mark.parametrize('test_case_name', [test_delect_department_case_name])
def test_delete_department(test_case_name, http_request):
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = departments.delete_department(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise




