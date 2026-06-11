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
        try :
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                jsonpath_expr=f"$..{balance_type}",
            )
            if result is None or len(result) != 4:
                logger.error("返回结果格式不正确")
                return None, None, None, None
            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'{balance_type}金额为:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("请求失败，无响应返回")
                return response, None, assert_code, case_id
        except Exception as e:
            logger.error(f"详情失败: {e}")


    #卡账户充值
    #首先获取admin设置的手续费率
    @classmethod
    def get_card_account_charge_rate(cls,http_request,test_case_name):
        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                jsonpath_expr="$.data",
            )
            if result is None or len(result) != 4:
                logger.error("返回结果格式不正确")
                return None, None, None, None
            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'手续费率为:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("请求失败，无响应返回")
                return response, None, assert_code, case_id
        except Exception as e:
            logger.error(f"详情失败: {e}"   )

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
