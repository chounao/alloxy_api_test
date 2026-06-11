# -*- coding: utf-8 -*-
import allure
import pytest
from api_processor.business_card.cardHolder import CardHolderManagement
import Common.assert_tools as assert_tools
from api_processor.common_function import common_data


card_holder = CardHolderManagement()
assert_tools = assert_tools.AssertTools()





test_get_department_id_case_name = '管理-获取部门列表'
@allure.epic("数字商务卡")
@allure.feature("持卡人模块")
@allure.story("查询部门列表")

@pytest.mark.parametrize(
    'test_case_name',
    [
        test_get_department_id_case_name
    ]
)
def test_get_department_id(http_request, test_case_name):
    with allure.step(f"执行测试: {test_case_name}"):
        result = card_holder.get_department_id(http_request, test_case_name)
        assert_tools._common_response_validation_code(result, test_case_name)






test_card_holder_list_case_name = '获取虚拟卡持有人列表'

@allure.epic("数字商务卡")
@allure.feature("持卡人")
@allure.story("获取虚拟卡持有人列表")
@pytest.mark.parametrize(
    'test_case_name,body',
    [
        (test_card_holder_list_case_name, {}),
        (test_card_holder_list_case_name, {'nickname': 'a'}),
        (test_card_holder_list_case_name, {'kyc_review_status': 'NA'}),
        (test_card_holder_list_case_name, {'kyc_review_status': 'COMPLETED'}),
        (test_card_holder_list_case_name, {'kyc_review_status': 'REJECTED'}),
        (test_card_holder_list_case_name, {'kyc_review_status': 'EXPIRED'}),
        (test_card_holder_list_case_name, {'kyc_review_status': 'RETRY'}),
        (test_card_holder_list_case_name, {'label': 'a'}),
        (test_card_holder_list_case_name, {'status': 'BAN'}),
        (test_card_holder_list_case_name, {'status': 'ACTIVE'}),
        # 合并部门ID筛选测试
        (test_card_holder_list_case_name, lambda http_request: {
            'rbac_department_id': card_holder.get_department_id_data(http_request)
        })
    ]
)
def test_card_holder_list(http_request, test_case_name, body):
    with allure.step(f"执行测试: {test_case_name}"):
        # 处理需要动态获取的body参数
        if callable(body):
            body = body(http_request)
        result = card_holder.get_card_holder_info(http_request, test_case_name, body)
        assert_tools._common_response_validation_code(result, test_case_name)


def test_get_list_data(http_request):
    with allure.step("获取虚拟卡持有人列表数据"):
        card_holder.get_card_holder_info_data(http_request)



test_card_holder_detail_case_name = '获取虚拟卡持有人详情'
@allure.epic("数字商务卡")
@allure.feature("持卡人模块")
@allure.story("获取虚拟卡持有人详情")
@pytest.mark.parametrize(
    'test_case_name,body',
    [(test_card_holder_detail_case_name, {'kyc_review_status': 'NA'}),
        (test_card_holder_detail_case_name, {'kyc_review_status': 'COMPLETED'}),
        (test_card_holder_detail_case_name, {'kyc_review_status': 'REJECTED'}),
        (test_card_holder_detail_case_name, {'kyc_review_status': 'EXPIRED'}),
        (test_card_holder_detail_case_name, {'kyc_review_status': 'RETRY'})]
)
def test_get_card_holder_detail(http_request, test_case_name,body):
    with allure.step(f"执行测试: {test_case_name}"):
        result = card_holder.operate_card_holder(http_request,body)
        assert_tools._common_response_validation_code(result, test_case_name)





test_card_holder_Freeze_case_name = '冻结虚拟卡持有人'
test_card_holder_Thawing_case_name = '解冻虚拟卡持有人'
@allure.epic("数字商务卡")
@allure.feature("持卡人模块")
@allure.story("冻结/解冻虚拟卡持有人")
@pytest.mark.parametrize(
    'test_case_name,body,status',
    [
        (test_card_holder_Freeze_case_name, {'kyc_review_status': 'COMPLETED'}, 'BAN'),
        (test_card_holder_Thawing_case_name, {'kyc_review_status': 'COMPLETED'}, 'ACTIVE'),
    ]
)
def test_freeze_or_thawing_card_holder(http_request, test_case_name, body, status):
    with allure.step(f"执行测试: {test_case_name}"):
        result = card_holder.freeze_or_thawing_card_holder(http_request, test_case_name, body)
        assert_tools._common_response_validation_code(result, test_case_name)




test_card_holder_delect_case_name = '删除虚拟卡持有人'
@allure.epic("数字商务卡")
@allure.feature("持卡人模块")
@allure.story("删除虚拟卡持有人")
@pytest.mark.parametrize(
    'test_case_name,body',
    [
        (test_card_holder_delect_case_name, {'kyc_review_status': 'COMPLETED'}),
    ]
)
def test_delete_card_holder(http_request, test_case_name, body,kyc_review_status):
    with allure.step(f"执行测试: {test_case_name}"):
        result = card_holder.operate_card_holder(http_request, test_case_name, body,kyc_review_status)
        assert_tools._common_response_validation_code(result, test_case_name)


test_get_params_case_name = '创建持卡人参数'
@allure.epic("数字商务卡")
@allure.feature("持卡人模块")
@allure.story("创建持卡人参数")
@pytest.mark.parametrize(
    'get_department_common,get_country_common,get_user_common',
    [
        ('测试部门', '不丹', 'ryan'),
    ],
    indirect=True
)
def test_get_params(http_request, get_department_common, get_country_common, get_user_common):
    with allure.step(f"执行测试：{test_get_params_case_name}"):
        department = get_department_common
        country = get_country_common
        user = get_user_common

        # 增加空值检查，防止因数据获取失败导致的后续崩溃
        if not all([department, country, user]):
            pytest.fail("前置数据获取失败：部门、国家或用户信息为空")

        result = card_holder.create_card_holder_params(department, user, country)





test_create_card_holder_case_name = '创建持卡人'
@allure.epic("数字商务卡")
@allure.feature("持卡人模块")
@allure.story("创建卡持有人")

@pytest.mark.parametrize(
    'get_department_common,get_country_common,get_user_common',
    [
        ('测试部门', '不丹', 'ryan'),
    ],
    indirect=True
)
def test_create_card_holder(http_request, get_department_common, get_country_common, get_user_common):
    with allure.step(f"执行测试：{test_create_card_holder_case_name}"):
        department = get_department_common
        country = get_country_common
        user = get_user_common

    result = card_holder.create_card_holder(http_request, test_create_card_holder_case_name,department, user, country)