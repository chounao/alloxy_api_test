import Common.logger as logger
from Common.simple_request import HttpRequest
from api_processor.wallet_model.wallet_list_page import WalletListPage
from Common.get_set_decimals import Decimals
import random

logger = logger.logger

class TransferOut:
    sheet_name = 'Wallte_page'
    wallet_list_page = WalletListPage()
    decimals = Decimals()


    @classmethod
    def get_crypto_payee_data(cls, test_case_name, http_request, from_currency, chain_name):
        """
        获取币种收款方数据
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :param from_currency: 要获取的币种
        :param chain_name: 要获取的链名称
        :return:
        """
        logger.info(f"Processing chain: {chain_name}, from_currency: {from_currency}")
        chain_data= cls.wallet_list_page.get_chain_data( http_request, chain_name)
        if chain_data is None:
            raise ValueError(f"未找到链名称 '{chain_name}' 对应的链数据")
        chain_id = chain_data['chain_id']
        # print(f"获取的链ID为：{chain_id}")
        try:
            data = {
                'page': 1,
                'take': 100,
                'currency': from_currency,
                'chain_id': chain_id,

            }
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                dict_data=data,
                nested_keys=['data', 'list']
            )
            if result is None or len(result) != 4:
                logger.error("获取用获取收款方请求返回结果格式不正确")
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            # print(extracted_parameters)
            if response is not None:
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("获取收款方请求失败，无响应返回")
                return response, None, assert_code, case_id
        except Exception as e:
            logger.error(f"获取收款方失败: {e}")
            raise e




    @classmethod
    def _get_payee_id(cls, http_request, from_currency, chain_name):
        """
        从收款方数据中提取指定币种的收款方ID

        :param extracted_parameters: 收款方数据列表
        :param from_currency: 要获取的币种
        :param chain_name: 要获取的链名称
        :return: 收款方ID或None
        """
        payee_list = []
        data = cls.get_crypto_payee_data('钱包-获取加密收款地址列表', http_request, from_currency, chain_name)
        if data is None:
            logger.error(f"未找到币种 '{from_currency}' 在链 '{chain_name}' 对应的收款方数据")
            return None
        else:
            response, extracted_parameters, assert_code,case_id = data
            if extracted_parameters is not None:
                for i in extracted_parameters:
                    if i['status'] == 'active':
                        payee_list.append(i['id'])
                if len(payee_list) > 0:
                    logger.info(f"获取的收款方ID列表为：{payee_list}")
                    return payee_list
                else:
                    logger.error(f"未找到币种 '{from_currency}' 在链 '{chain_name}' 对应的收款方ID")
                    return None
            else:
                logger.error("获取收款方请求失败，无响应返回")
                return None



    @classmethod
    def get_crypto_withdraw_fee_data(cls, test_case_name, http_request, from_currency):
        """
        获取币种提现手续费数据
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :param from_currency: 要获取的币种
        :param chain_name: 要获取的链名称
        :return:
        """

        try:
            data = {
                'feeType': 'crypto_withdraw_fee',
                'condition': from_currency,

            }

            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                dict_data=data,
                nested_keys=['data', 'number']
            )
            if result is None or len(result) != 4:
                logger.error("获取用获取提现手续费请求返回结果格式不正确")
                return None, None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            # after_amount = cls.wallet_list_page.get_from_currency_data(http_request,from_currency)
            if extracted_parameters is not None:
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("获取提现手续费请求失败，无响应返回")
                return response, None, assert_code, case_id
        except Exception as e:
            logger.error(f"获取提现手续费失败: {e}")
            raise e

    @classmethod
    def get_transfer_out_fee(cls,  http_request, from_currency):
        """
        获取转账手续费
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :param from_currency: 要转账的币种
        :param chain_id: 要转账的链ID
        :param amount: 转账金额
        :param to_address: 收款地址
        :return:
        """
        response, extracted_parameters, assert_code, case_id = cls.get_crypto_withdraw_fee_data('钱包-转出费率', http_request, from_currency)
        if extracted_parameters is not None:
            # decimal_places = cls.decimals._get_decimals_for_crypto(currency =from_currency,decimal_str = extracted_parameters)
            # if decimal_places is  not None:
            #     return  decimal_places
            return extracted_parameters

            # else:
            #     logger.error(f"获取币种 {from_currency} 的小数位数失败")
            #     return None

        else:
            logger.error("获取转账手续费请求失败，无响应返回")
            return None
    @classmethod
    def _get_transfer_out_handling_fee(cls, test_case_name, http_request,chain_name):
        """
        获取提币手续费：后台设置的
        :param http_request:
        :param from_currency:
        :param chain_name:
        :return:
        """

        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                jsonpath_expr= f"$.data.list[*].chain_fee[?(@.chain_name=='{chain_name}')].fee"
            )
            if result is None or len(result) != 4:
                logger.error("获取提币手续费请求返回结果格式不正确")
                return None, None, None, None, None

            response, extracted_parameters, assert_code, case_id = result

            if extracted_parameters is not None:
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("获取提币手续费请求失败，无响应返回")
                return response, None, assert_code, case_id
        except Exception as e:
            logger.error(f"获取提币手续费失败: {e}")
            raise e

    @classmethod
    def transfer_out_handling_fee(cls,http_request,chain_name,price):
        """
        获取提币手续费：后台设置的
        :param http_request:
        :param chain_name:
        :return:
        """

        response, extracted_parameters, assert_code, case_id = cls._get_transfer_out_handling_fee('获取后台设置的转出手续费', http_request, chain_name)
        #把str类型转成float类型
        price = float(price)
        print(price)
        handling_fee = extracted_parameters * price

        return handling_fee

    @classmethod
    def transfer_out_data(cls,  http_request, from_currency, chain_name, amount):
        """
        获取转账数据
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :param from_currency: 要转账的币种
        :param chain_id: 要转账的链ID
        :param amount: 转账金额
        :param to_address: 收款地址
        :return:
        """
        logger.info(f"Processing chain: {chain_name}, from_currency: {from_currency}")
        payee_list = cls._get_payee_id( http_request, from_currency, chain_name)
        if payee_list is None:

            return None
        else:
            payee_id =random.choice(payee_list)
        chain_id = cls.wallet_list_page.get_chain_data(http_request, chain_name)['chain_id']

        wallet_id = WalletListPage.get_currency_data(http_request, from_currency)
        logger.info(f"获取的钱包ID为：{wallet_id['id']}")
        logger.info(f"获取的链ID为：{chain_id}")
        #如果amount不是float类型转换为float
        if not isinstance(amount, float):
            amount = float(amount)
        variables_body= {"wallet_id": wallet_id['id'],
                "chain_id": chain_id,
                "payee_id": payee_id,
                "amount": amount,
                }

        return variables_body


    @classmethod
    def _transfer_out_pass(cls, variables, test_case_name, http_request):
        """
        执行转账操作
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :param variables: 转账参数
        :return:
        """
        # 添加日志查看传入的参数


        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                variables
            )


            if result is None or len(result) != 4:
                logger.error("转账请求返回结果格式不正确")
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                return response, None, assert_code, case_id
            else:
                logger.error("转账请求失败，无响应返回")
                return None, None, None, None
        except Exception as e:
            logger.error(f"转账失败: {e}")
            raise e

    @classmethod
    def _transfer_out_fail(cls, variables, test_case_name, http_request):
        """
        执行转账操作
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :param variables: 转账参数
        :return:
        """
        # 添加日志查看传入的参数

        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                dict_data=variables
            )
            print(result)
            if result is None or len(result) != 4:
                logger.error("转账请求返回结果格式不正确")
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                return response, None, assert_code, case_id
            else:
                logger.error("转账请求失败，无响应返回")
                return None, None, None, None
        except Exception as e:
            logger.error(f"转账失败: {e}")
            raise e


if __name__ == '__main__':
    http_request = HttpRequest ()
    TransferOut.transfer_out_data('测试用例名称', http_request, 'USDT', 'arbitrum', '0.01')
