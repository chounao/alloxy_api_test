import allure
import pytest

from Common.case_runner import case_runner


@allure.epic("示例模块")
@allure.feature("统一执行器示例")
@pytest.mark.priority("high")
@pytest.mark.parametrize("test_case_name", ["首页-账户信息统计"])
def test_home_overview_demo(http_request, test_case_name):
    """示例：使用 CaseRunner 执行接口用例。

    中文备注：真实落地时，把业务方法替换为当前模块 processor 的方法即可。
    """
    return case_runner.run_api_case(
        case_name=test_case_name,
        func=http_request.execute_case,
        sheet_name="Home_page",
        test_case_name=test_case_name,
        response_rules=[
            {"jsonpath": "$.data", "operator": "not_empty"},
        ],
    )
