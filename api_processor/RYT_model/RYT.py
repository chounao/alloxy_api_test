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


        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name)
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
            test_case_name=test_case_name)



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
            test_case_name=test_case_name)



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
            test_case_name=test_case_name)



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
            test_case_name=test_case_name)



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
            })



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
        })
