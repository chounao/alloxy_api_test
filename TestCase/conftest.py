# -*- coding: utf-8 -*-

import pytest
from api_processor.wallet_model.payee import Payee
from api_processor.common_function import common_data
from api_processor.login import Alloxy_login
from api_processor.wallet_model.wallet_list_page import WalletListPage
from api_processor.business_card import Card_account_Management

from Common.execute import set_env
from Common import logger
import Common.simple_request


logger = logger.logger




def pytest_addoption(parser: pytest.Parser) -> None:
    """pytest 钩子：添加命令行参数"""
    # 添加环境参数（支持 --env 指定）
    parser.addoption(
        "--env",
        action="store",
        default="test",
        choices=["test", "uat", "prod"],  # 限制可选值，避免无效输入
        help="指定测试环境：test（默认）/uat/prod"
    )
    # 添加优先级参数（支持 --priority 过滤用例）
    parser.addoption(
        "--priority",
        action="store",
        default="all",
        choices=["high", "medium", "low", "all"],  # 限制可选值
        help="指定用例优先级：high/medium/low/all（默认）"
    )

@pytest.fixture(scope="session", autouse=True)
def global_env_setup(request: pytest.FixtureRequest) -> None:
    """
    全局环境初始化 fixture（自动执行，无需手动调用）
    作用：在测试会话开始前，根据命令行参数设置环境
    """
    # 从命令行参数获取环境（默认 test）
    env = request.config.getoption("--env")
    # 初始化环境
    set_env(env)
    logger.info(f"---测试开始---执行的是 {env} 环境")
    # 测试结束后可添加清理逻辑
    yield
    logger.info(f"---测试结束---{env} 环境执行完毕")


@pytest.fixture(scope="function")
def priority_filter(request: pytest.FixtureRequest) -> None:
    """
    用例优先级过滤 fixture（根据 --priority 参数跳过不符合的用例）
    使用方式：在测试用例上添加 @pytest.mark.priority("high") 标记
    """
    # 获取命令行指定的优先级
    target_priority = request.config.getoption("--priority")
    if target_priority == "all":
        return  # 不过滤，执行所有用例

    # 获取当前用例的优先级标记（若未标记，默认视为 low）
    case_priority = request.node.get_closest_marker("priority")
    case_priority = case_priority.args[0] if case_priority else "low"

    # 若用例优先级与目标不符，跳过用例
    if case_priority != target_priority:
        pytest.skip(f"用例优先级为 {case_priority}，跳过（目标：{target_priority}）")

@pytest.fixture(scope="session")
def http_request():
    """提供全局的 HTTP 请求实例"""
    return Common.simple_request.HttpRequest()
@pytest.fixture(scope="session", autouse=True)
def login_setup(http_request):
    """
    登录前置处理器：在测试模块执行前完成登录，返回 access_token
    复用"登录成功"的测试数据和逻辑
    """
    logger.info("---前置处理器开始---")
    try:
        login = Alloxy_login()
        # request_ = Common.simple_request.HttpRequest()
        variables_pass, variables_lost_password, variables_lost_email = login.get_login_data()

        result = login.login('登陆成功',variables_pass)  # 注意用例名称要匹配
        if result is None or len(result) != 4:
            pytest.fail("前置处理器登录失败，无法执行后续用例")

        access_token, response_status_code, assert_code,case_id= result
        if response_status_code != 201:
            pytest.fail("前置处理器登录失败，无法执行后续用例")
        if access_token is None:
            pytest.fail("前置处理器登录失败，无法执行后续用例")
        else:
            http_request.update_headers({
                'authorization': f'Bearer {access_token}'
            })
            logger.debug(f"更新后的请求头: {http_request.headers}")
            return access_token
    except Exception as e:
        pytest.fail(f"前置处理器执行异常: {str(e)}")


def pytest_collection_modifyitems(session, config, items):
    """过滤用例（只保留符合优先级的用例）"""
    priority = config.getoption("--priority")
    if priority == "all":
        return  # 不过滤

    # 筛选出符合优先级的用例（假设用例名包含"_high_"等标识）
    filtered_items = []
    for item in items:
        if priority == "high" and "_high_" in item.nodeid:
            filtered_items.append(item)
        elif priority == "medium" and "_medium_" in item.nodeid:
            filtered_items.append(item)
        elif priority == "low" and "_low_" in item.nodeid:
            filtered_items.append(item)

    # 替换用例列表（只执行过滤后的用例）
    items[:] = filtered_items
    logger.info(f"已过滤用例，只保留 {priority} 优先级，共 {len(items)} 条")

# 1. 处理用例收集阶段的中文编码（核心）
def pytest_collection_modifyitems(items):
    """修复中文用例名称乱码（收集阶段处理一次）"""
    for item in items:
        # 处理用例名称
        item.name = item.name.encode('latin-1').decode('unicode_escape')
        # 处理 nodeid（文件路径+用例名）
        item._nodeid = item.nodeid.encode('latin-1').decode('unicode_escape')


# 2. 自定义报告输出（直接使用已处理的 nodeid）
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # 直接使用 item.nodeid（已被 pytest_collection_modifyitems 处理过的中文）
        nodeid = item.nodeid
        if report.failed:
            logger.error(f"用例 {nodeid} 执行失败！")
        elif report.passed:
            logger.info(f"用例 {nodeid} 执行通过")
def pytest_configure(config):
    config.addinivalue_line("markers", "priority: mark test with priority level (high, medium, low)")
















"""

获取前置的一些操作方法，比如获取钱包数据，获取chain数据，获取国家地址信息，获取部门，获取用户
"""

@pytest.fixture(scope="function")
def before_wallet_data_out_type(http_request,from_currency):
    """只为特定测试执行的前置方法"""
    logger.info("在执行前获取钱包的数据")
    wallet_list_page = WalletListPage()
    data = wallet_list_page.get_currency_data(http_request,from_currency)
    # print(f"获取的数据为：{data['id']}")
    yield  data




@pytest.fixture(scope="function")
def before_wallet_data_in_type(http_request,to_currency):
    """只为特定测试执行的前置方法"""
    logger.info("在执行前获取钱包的数据")
    wallet_list_page = WalletListPage()
    data = wallet_list_page._get_currency_data(http_request,to_currency)
    # print(f"获取的数据为：{data['id']}")
    yield  data



@pytest.fixture(scope="function")
def get_chain_list_data(http_request,chain_name):
    logger.info("获取链列表数据")
    wallet_list_page = WalletListPage()
    chain_data =wallet_list_page.get_chain_data(http_request,chain_name)
    yield chain_data



@pytest.fixture(scope="function")
def get_department_common(http_request, request):
    logger.info("获取部门ID")
    department_name = request.param
    common_tools = common_data.GetCommonData()
    # 假设 get_department_data 返回元组，取第二个元素；根据实际情况调整
    result = common_tools.get_department_data(http_request, '获取部门信息', department_name)
    yield result[1] if result else None


@pytest.fixture(scope="function")
def get_country_common(http_request, request):
    logger.info("获取国家ID")
    country_name = request.param
    common_tools = common_data.GetCommonData()
    result = common_tools.get_data_for_country(http_request, '获取国家/地址信息', country_name)
    yield result[1] if result else None


@pytest.fixture(scope="function")
def get_user_common(http_request, request):
    logger.info("获取用户ID")
    first_name = request.param
    common_tools = common_data.GetCommonData()
    result = common_tools.get_user_id(http_request, '获取用户信息', first_name)
    yield result[1] if result else None



# balance_type = 'cardAccountBalance'
# balance_type = 'cardBalance'
@pytest.fixture(scope="function")
def get_card_balance(http_request,balance_type):
    logger.info("获取卡账户余额和卡余额")
    card_management = Card_account_Management.CardAccountManagement()
    result = card_management.get_cardAccountBalance_and_cardBalance(http_request, balance_type)
    yield result




