# -*- coding: utf-8 -*-
import allure
import pytest
from api_processor.login import Alloxy_login
import Common.assert_tools as assert_tools


login = Alloxy_login()
assert_tools = assert_tools.AssertTools()

# 测试用例参数配置获取到login_test_cases中的数据
variables_pass,variables_lost_password,variables_lost_email = login.get_login_data()

@allure.epic("登录功能")
@allure.feature("用户登录")
@pytest.mark.parametrize('test_case_name,variables', [
    ('登陆成功', variables_pass),
    ('密码错误', variables_lost_password),
    ('邮箱错误', variables_lost_email)
])
@pytest.mark.priority("high")
def test_login(test_case_name, variables):
    """
    测试登录功能（数据驱动，支持批量执行）
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :param variables: 登录参数（email/password）


    """
    with allure.step(f"执行登录测试: {test_case_name}"):
        result = login.login(test_case_name, variables)

        # 检查登录函数是否正常返回
        if result is None or len(result) != 4:
            allure.attach("登录接口调用失败", name="登录异常")
            pytest.fail("登录接口调用失败，返回结果格式不正确")

        # 解包返回结果
        access_token, response_status_code, assert_code,case_id = result

        # 检查响应状态码是否存在
        if response_status_code is None:
            allure.attach("无响应状态码", name="登录异常")
            pytest.fail("登录接口无响应状态码")

        # 根据测试用例名称进行不同的断言处理
        try:
            assert_tools.assert_status_code(assert_code, response_status_code)
            if access_token:
                allure.attach(str(response_status_code), name="登录成功状态码")
                allure.attach(access_token, name="访问令牌")
            else:
                allure.attach(str(response_status_code), name="登录失败状态码")
        except AssertionError:
            allure.attach(str(response_status_code), name="状态码断言失败")
            pytest.fail(f"状态码断言失败: 期望{assert_code}, 实际{response_status_code}")
        # assert_tools._common_response_validation_code(result, test_case_name)



if __name__ == '__main__':
    pytest.main(["-s", "--env", "test", "--priority", "high", "--collect-only",
                 "/Users/alloyx/Desktop/alloxy_api_testcase_framework/TestCase/test_login.py"])
