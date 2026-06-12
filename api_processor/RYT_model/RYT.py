import Common.logger as logger
logger = logger.logger

class Ryt:
    sheet_name = 'RYT_page'


    #获取账户信息
    @classmethod
    def get_account_info(cls,http_request,test_case_name):
        """
        获取账户信息
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 账户信息
        """
        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                # jsonpath_expr="$.data",
            )
            if result is None or len(result) != 4:
                logger.error("返回结果格式不正确")
                return None, None, None, None
            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'获取的账户信息为:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("请求失败，无响应返回")
                return response, None, assert_code, case_id
        except Exception as e:
            logger.error(f"详情失败: {e}")

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            error_msg="获取账户信息失败")
    #获取供应量信息
    @classmethod
    def get_supply_info(cls,http_request,test_case_name):
        """
        获取供应量信息
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 供应量信息
        """

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            error_msg="获取供应量信息失败")



    #获取价格列表信息
    @classmethod
    def get_price_list_info(cls,http_request,test_case_name):
        """
        获取价格列表信息
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 价格列表信息
        """
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            error_msg="获取价格列表信息失败")


    #获取利润清单信息
    @classmethod
    def get_profit_list_info(cls,http_request,test_case_name):
        """
        获取利润清单信息
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 利润清单信息
        """


        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            error_msg="获取利润清单信息失败")



    #获取交易记录
    @classmethod
    def get_transaction_record(cls,http_request,test_case_name):
        """
        获取交易记录
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 交易记录
        """


        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            error_msg="获取交易记录失败")



    #购买ryt
    @classmethod
    def buy_ryt(cls,http_request,test_case_name,amount):
        """
        购买ryt
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 购买ryt结果
        """

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables={
                "amount": amount
            },
            error_msg="购买ryt失败")



    #赎回RYT
    @classmethod
    def sell_ryt(cls,http_request,test_case_name,amount):
        """
        赎回RYT
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 赎回RYT结果
        """

        return http_request.execute_case(
        sheet_name=cls.sheet_name,
        test_case_name=test_case_name,
        variables={
            "amount": amount
        },
        error_msg="赎回RYT失败")