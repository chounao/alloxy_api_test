# -*- coding: utf-8 -*-
import allure
import pytest
from api_processor.approval_model import approval
import Common.assert_tools as assert_tools

approval = approval.Approval()
assert_tools = assert_tools.AssertTools()

test_get_approval_list_case_name_for_pending = '获取审批列表'
@allure.epic("审批")
@allure.feature("审批模块")
@allure.story("获取审批列表")

def test_get_approval_list_for_pending(http_request):
    with allure.step(f"执行测试: {test_get_approval_list_case_name_for_pending}"):
        result = approval.get_approval_data_for_pending(http_request, test_get_approval_list_case_name_for_pending)
        assert_tools._common_response_validation_code(result, test_get_approval_list_case_name_for_pending)








test_operation_approval_case_name = '操作审批'
@allure.epic("审批")
@allure.feature("审批模块")
@allure.story("操作审批")
@pytest.mark.parametrize(
    'test_case_name,approval_status',
    [
        (test_operation_approval_case_name, 'approved'),
        (test_operation_approval_case_name, 'rejected')
    ]
)
def test_operation_approval(http_request, test_case_name, approval_status):
    with allure.step(f"执行测试: {test_operation_approval_case_name}"):
        result = approval.operation_approval(http_request, test_case_name, approval_status)
        assert_tools._common_response_validation_code(result, test_operation_approval_case_name)







test_get_approval_list_case_name_for_approved= '获取已办列表'
@allure.epic("审批")
@allure.feature("审批模块")
@allure.story("获取审批列表")

def test_get_approval_list_for_approved(http_request):
    with allure.step(f"执行测试: {test_get_approval_list_case_name_for_approved}"):
        result = approval.get_approval_data_for_approved(http_request, test_get_approval_list_case_name_for_approved)
        assert_tools._common_response_validation_code(result, test_get_approval_list_case_name_for_approved)