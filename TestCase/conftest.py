# -*- coding: utf-8 -*-

import allure
import pytest

from Common import logger
from Common.execute import set_env
from Common.simple_request import HttpRequest


logger = logger.logger


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--env", action="store", default="test", choices=["test", "uat", "prod"],
                     help="指定测试环境: test/uat/prod")
    parser.addoption("--priority", action="store", default="all", choices=["high", "medium", "low", "all"],
                     help="按priority标记过滤用例")


def pytest_configure(config):
    config.addinivalue_line("markers", "priority(level): mark test priority: high, medium, low")


def _decode_node_id(item) -> None:
    try:
        item.name = item.name.encode("latin-1").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("latin-1").decode("unicode_escape")
    except UnicodeError:
        pass


def pytest_collection_modifyitems(session, config, items):
    # 中文备注：合并中文 nodeid 修复和 priority 过滤，避免重复定义 hook 互相覆盖。
    target_priority = config.getoption("--priority")
    selected = []

    for item in items:
        _decode_node_id(item)
        marker = item.get_closest_marker("priority")
        case_priority = marker.args[0] if marker and marker.args else "low"
        item.user_properties.append(("priority", case_priority))
        if target_priority == "all" or case_priority == target_priority:
            selected.append(item)

    if target_priority != "all":
        deselected = [item for item in items if item not in selected]
        config.hook.pytest_deselected(items=deselected)
        items[:] = selected
        logger.info("已按priority=%s过滤用例，共保留%s条", target_priority, len(items))


@pytest.fixture(scope="session", autouse=True)
def global_env_setup(request: pytest.FixtureRequest):
    env = request.config.getoption("--env")
    set_env(env)
    logger.info("---测试开始---执行环境: %s", env)
    yield
    logger.info("---测试结束---执行环境: %s", env)


@pytest.fixture(scope="session")
def http_request():
    # 中文备注：整个测试会话复用一个 requests.Session，提高接口执行效率。
    request_client = HttpRequest()
    yield request_client
    request_client.session.close()
    request_client.excel.close()


@pytest.fixture(scope="session", autouse=True)
def login_setup(http_request):
    # 中文备注：全局登录只执行一次，并把 token 写入共享 HTTP 客户端请求头。
    from api_processor.login import Alloxy_login

    logger.info("---登录前置开始---")
    with allure.step("全局登录前置"):
        login = Alloxy_login()
        variables_pass, _, _ = login.get_login_data()
        result = login.login("登陆成功", variables_pass)
        if result is None or len(result) != 4:
            pytest.fail("前置登录失败: 返回结构异常")

        access_token, response_status_code, assert_code, case_id = result
        allure.attach(str(case_id), name="登录用例ID", attachment_type=allure.attachment_type.TEXT)
        if int(response_status_code) != int(assert_code):
            pytest.fail(f"前置登录失败: 期望状态码{assert_code}, 实际{response_status_code}")
        if not access_token:
            pytest.fail("前置登录失败: access_token为空")

        token_value = str(access_token)
        if not token_value.lower().startswith("bearer "):
            token_value = f"Bearer {token_value}"
        http_request.update_headers({"authorization": token_value})
    logger.info("---登录前置完成---")
    return access_token


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    if report.failed:
        logger.error("用例执行失败: %s", item.nodeid)
    elif report.passed:
        logger.info("用例执行通过: %s", item.nodeid)


@pytest.fixture(scope="function")
def before_wallet_data_out_type(http_request, from_currency):
    from api_processor.wallet_model.wallet_list_page import WalletListPage

    logger.info("获取转出钱包数据: %s", from_currency)
    yield WalletListPage().get_currency_data(http_request, from_currency)


@pytest.fixture(scope="function")
def before_wallet_data_in_type(http_request, to_currency):
    from api_processor.wallet_model.wallet_list_page import WalletListPage

    logger.info("获取转入钱包数据: %s", to_currency)
    yield WalletListPage()._get_currency_data(http_request, to_currency)


@pytest.fixture(scope="function")
def get_chain_list_data(http_request, chain_name):
    from api_processor.wallet_model.wallet_list_page import WalletListPage

    yield WalletListPage().get_chain_data(http_request, chain_name)


@pytest.fixture(scope="function")
def get_department_common(http_request, request):
    from api_processor.common_function.common_data import GetCommonData

    result = GetCommonData().get_department_data(http_request, "获取部门信息", request.param)
    yield result[1] if result else None


@pytest.fixture(scope="function")
def get_country_common(http_request, request):
    from api_processor.common_function.common_data import GetCommonData

    result = GetCommonData().get_data_for_country(http_request, "获取国家/地址信息", request.param)
    yield result[1] if result else None


@pytest.fixture(scope="function")
def get_user_common(http_request, request):
    from api_processor.common_function.common_data import GetCommonData

    result = GetCommonData().get_user_id(http_request, "获取用户信息", request.param)
    yield result[1] if result else None


@pytest.fixture(scope="function")
def get_card_balance(http_request, balance_type):
    from api_processor.business_card.Card_account_Management import CardAccountManagement

    yield CardAccountManagement().get_cardAccountBalance_and_cardBalance(http_request, balance_type)
