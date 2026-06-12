from random import random
import Common.logger as logger


logger = logger.logger
class CardAccountManagement:
    sheet_name = 'Card_page'


    @classmethod
    def get_cardAccountBalance_and_cardBalance(cls,http_request, test_case_name,balance_type):
        """
        获取持卡人余额和卡账户余额
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 持卡人余额/卡账户余额
        """
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            jsonpath_expr=f"$..{balance_type}"
        )


    #卡账户充值
    #首先获取admin设置的手续费率
    @classmethod
    def get_card_account_charge_rate(cls,http_request,test_case_name):

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            jsonpath_expr="$.data"
        )
    #传参
    @classmethod
    def card_account_recharge_params(cls,wallet_id,from_currency, amount):
        body = {"wallet_id": wallet_id,
                "from_currency": from_currency,
                "amount": amount,
                "memo": "123",
                "to_currency": "USD"}
        print( body)

    # 卡账户充值
    @classmethod
    def card_account_recharge(cls,http_request,test_case_name,from_currency,amount):
        body = {"wallet_id":"e56f09e4-e2cc-4453-a513-3b90d565fa18",
                "from_currency":from_currency,
                "amount":amount,
                "memo":"123",
                "to_currency":"USD"}

    #卡账户转出
