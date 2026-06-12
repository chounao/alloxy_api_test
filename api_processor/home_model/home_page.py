import random
from Common.simple_request import HttpRequest
import Common.logger as logger
logger = logger.logger


class HomePage:
    sheet_name = 'Home_page'

    @classmethod
    def get_user_data(cls, http_request, test_case_name):
        """获取登录数据"""
        return http_request.execute_case(sheet_name=cls.sheet_name,
            test_case_name=test_case_name)

    @classmethod
    def get_user_menus(cls, http_request, test_case_name):
        """获取用户菜单权限"""
        return http_request.execute_case(sheet_name=cls.sheet_name,
            test_case_name=test_case_name)

    @classmethod
    def get_user_account_overview(cls, http_request, test_case_name, data_type=None, filter_key=None, filter_value=None):
        """
        获取用户账户概览

        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :param data_type: 数据类型 ('balance_list', 'transaction_list' 或 None)
        :param filter_key: 筛选键名
        :param filter_value: 筛选值
        :return: tuple(response, extracted_parameters, assert_code, case_id)
        """
        response, extracted_parameters, assert_code, case_id = http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name
        )

        if data_type is None:
            return response, extracted_parameters, assert_code, case_id

        if not response or not extracted_parameters:
            logger.warning(f"[{test_case_name}] 获取账户概览数据为空")
            return response, extracted_parameters, assert_code, case_id

        account_overview = extracted_parameters

        if data_type == 'balance_list':
            for item in account_overview:
                if item.get(filter_key) == filter_value:
                    logger.info(f"[{test_case_name}] 找到匹配的balance")
                    return response, item, assert_code, case_id
            logger.warning(f"[{test_case_name}] 未找到匹配的balance")
            return response, None, assert_code, case_id

        elif data_type == 'transaction_list':
            pending_ids = [item.get(filter_key) for item in account_overview
                          if item.get('status') == 'pending' and item.get(filter_key)]
            logger.info(f"[{test_case_name}] 找到{len(pending_ids)}个pending状态的交易ID")
            return response, pending_ids, assert_code, case_id

        return response, extracted_parameters, assert_code, case_id

    @classmethod
    def get_todo_data(cls, http_request, test_case_name):
        """获取待办数据"""
        return http_request.execute_case(sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            nested_keys=['data'])

    @classmethod
    def get_notices(cls, http_request, test_case_name):
        """获取用户通知"""
        return http_request.execute_case(sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            nested_keys=['data'])
    @classmethod
    def get_transacton_detail(cls, http_request, test_case_name, transaction_id):
        """获取用户交易详情"""
        return http_request.execute_case(sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            replace_data=transaction_id)

    @classmethod
    def _get_transaction_id(cls, http_request):
        """
        获取随机交易ID

        :param http_request: HTTP请求实例
        :return: 随机选择的交易ID，失败时返回None
        """
        try:
            result = cls.get_user_account_overview(http_request, '账号信息统计', 'transaction_list', 'id')
            if result is None or len(result) != 4:
                logger.error("获取交易ID请求返回结果格式不正确")
                return None

            response, transaction_id_list, assert_code, case_id = result

            if not transaction_id_list:
                logger.error("获取交易ID失败，无交易记录")
                return None

            return random.choice(transaction_id_list)

        except Exception as e:
            logger.error(f"获取交易ID失败: {e}")
            return None


if __name__ == '__main__':
    home = HomePage()
    http_request = HttpRequest()
    home._get_transaction_id(http_request)