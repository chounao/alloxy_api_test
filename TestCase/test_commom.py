# -*- coding: utf-8 -*-
import allure
import pytest

from TestCase.test_card_holders import test_get_department_id
from api_processor.common_function import common_data
import Common.assert_tools as assert_tools


common_tools = common_data.GetCommonData()
assert_tools = assert_tools.AssertTools()

test_get_country_info_case_name = '获取国家/地址信息'
@allure.epic("管理页面")
@allure.feature("组织架构")
@pytest.mark.priority("high")
@pytest.mark.parametrize('test_case_name', [test_get_country_info_case_name])
def test_get_country_info(test_case_name, http_request):
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = common_tools.get_country_info_data(http_request, test_case_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise




# TEST_COUNTRY_DATA = [
#     ('中国台湾')
# ]
country = '不丹'
@allure.epic("管理页面")
@allure.feature("组织架构")
@pytest.mark.priority("high")
@pytest.mark.parametrize('test_case_name,country', [(test_get_country_info_case_name, country)])
def test_get_get_data_for_country(test_case_name, http_request, country):
    with allure.step(f"执行测试：{test_case_name} - 国家：{country}"):
        try:
            allure.attach(f"测试参数：country={country}", name="测试输入")
            result = common_tools.get_data_for_country(http_request, test_case_name, country)
            allure.attach(f"响应结果：{result}", name="测试结果")
            assert_tools._common_response_validation_code(result, test_case_name)
        except AssertionError as e:
            allure.attach(f"断言失败：{str(e)}", name="断言异常")
            raise
        except Exception as e:
            allure.attach(f"测试执行异常：{str(e)}", name="异常信息")
            allure.attach(f"失败时参数：country={country}", name="异常上下文")
            raise





department_name = '测试部门'
test_get_department_data = '获取部门信息'
@allure.epic("管理页面")
@allure.feature("组织架构")
@pytest.mark.priority("high")
@pytest.mark.parametrize('test_case_name,department_name', [(test_get_department_data,department_name)])
def test_get_department_id(http_request,test_case_name,department_name):
    with allure.step(f"执行测试：获取部门ID"):
        try:
            result = common_tools.get_department_data(http_request,test_case_name,department_name)
            assert_tools._common_response_validation_code(result, test_case_name)
            return result
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise


first_name ='ryan'
test_get_user_data = '获取用户信息'
@allure.epic("管理页面")
@allure.feature("组织架构")
@pytest.mark.priority("high")
@pytest.mark.parametrize('test_case_name,user_name', [(test_get_user_data,first_name)])
def test_get_user_id(http_request,test_case_name,user_name):
    with allure.step(f"执行测试：获取用户ID"):
        try:
            result = common_tools.get_user_id(http_request,test_case_name,user_name)
            assert_tools._common_response_validation_code(result, test_case_name)
            return result
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise