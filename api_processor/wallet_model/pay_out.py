from pydoc import pager
from Common.simple_request import HttpRequest
import Common.logger as logger
import math
from Common.read_and_save_tool import ConfigTools
from Common.get_set_decimals import Decimals
from api_processor.wallet_model.wallet_list_page import WalletListPage
logger = logger.logger


class PayOut:
    wallet_list_page = WalletListPage()
    sheet_name = 'Wallte_page'
    decimals = Decimals()
    config = ConfigTools()
    @classmethod
    def get_fiat_fee_info(cls, http_request, test_case_name,id =None):
        """
        获取法币到 crypto 的手续费
        :param http_request:
        :param test_case_name:
        :return:
        """

        data = f'id={id}'

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            ping_data=data,
            nested_keys=['data'],
            error_msg="获取加密货币到法币手续费失败")

    @classmethod
    def get_country_rate_data(cls, http_request,from_currency,id):
        result = cls.get_fiat_fee_info(http_request, '获取加密货币到法币手续费',id)
        if result is None:
            return None
        response, extracted_parameters, assert_code, case_id = result
        print(f'获取加密货币到法币手续费参数是:{extracted_parameters}')
        # 添加空值检查


        rate_fee = float(extracted_parameters['rate'][from_currency])
        per_count = float(extracted_parameters['per_count'])
        prorate = float(extracted_parameters['prorate'])
        network_per_fee = float(extracted_parameters['network_per_fee'])
        network_prorate_fee = float(extracted_parameters['network_prorate_fee'])
        # rate_fee = cls.decimals._get_decimals_for_fiat(to_currency,extracted_parameters['rate'][to_currency])

        # per_count = cls.decimals._get_decimals_for_crypto(from_currency,extracted_parameters['per_count'])

        # prorate = cls.decimals._get_decimals_for_crypto(from_currency,extracted_parameters['prorate'])

        # network_per_fee = cls.decimals._get_decimals_for_crypto(from_currency,extracted_parameters['network_per_fee'])
        # network_prorate_fee = cls.decimals._get_decimals_for_crypto(from_currency,extracted_parameters['network_prorate_fee'])

        print(f'汇率手续费:{rate_fee},'
              f'每笔手续费:{per_count},'
              f'比例手续费:{prorate},'
              f'网络每笔手续费:{network_per_fee},'
              f'网络比例手续费:{network_prorate_fee}')

        return rate_fee, per_count, prorate,network_per_fee,network_prorate_fee




    @classmethod
    def get_fiat_rate_info(cls, http_request, test_case_name,from_currency,to_currency):
        """
        获取法币汇率
        :param http_request:
        :param test_case_name:
        :param from_currency:
        :param to_currency:
        :return:
        """
        data = {
                'from_currency':from_currency,
                'to_currency': to_currency}

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            dict_data=data,
            nested_keys=['data'],
            error_msg="获取法币汇率失败")
    @classmethod
    def get_rate_data(cls, http_request, from_currency,to_currency):
        result = cls.get_fiat_rate_info(http_request, '获取pay_out汇率',from_currency,to_currency)
        if result is None:
            return None
        response, extracted_parameters, assert_code, case_id = result
        rate_data = extracted_parameters
        return rate_data


    @classmethod
    def get_payee_info(cls, http_request, test_case_name,to_currency):
        """
        获取法币收款地址
        :param http_request:
        :param test_case_name:
        :param to_currency:
        :return:
        """
        data = {
            'currency': to_currency,
            'payee_name' : '',
            'page' : 1,
            'take' : 100,
            'status' : 'active'

        }
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            dict_data=data,
            nested_keys=['data', 'list', 0, 'id'],
            error_msg="获取法币收款地址失败")

    @classmethod
    def get_payee_address(cls, http_request,to_currency):
        result = cls.get_payee_info(http_request, '钱包-获取法币收款地址列表',to_currency)
        if result is None:
            return None
        response, extracted_parameters, assert_code, case_id = result
        payee_id = extracted_parameters

        return payee_id

    @classmethod
    def pay_out_parameter(cls, http_request, from_currency, to_currency, amount, memo):
        """
        获取提现参数
        :param http_request:
        :param from_currency:
        :param to_currency:
        :param amount:
        :param memo:
        :return:
        """

        # 汇率
        to_currency_rate = cls.get_rate_data(http_request, from_currency, to_currency)
        logger.info(f"获取汇率: {to_currency_rate}")

        if to_currency_rate is None:
            logger.error("汇率获取失败")
            return None

        # 验证金额有效性
        # 优化后的金额验证逻辑
        logger.info(f"验证金额: {amount}, 类型: {type(amount)}")

        # 检查amount是否为数字类型（整数或浮点数）
        if not isinstance(amount, (int, float)):
            logger.error("金额无效，不是数字类型")
            return None

        # 如果amount小于等于0，则赋值为1
        if amount <= 0:
            logger.warning(f"金额{amount}小于等于0，已自动设置为1")
            amount = 1

        # 验证汇率有效性
        logger.info(f"验证汇率: {to_currency_rate}, 类型: {type(to_currency_rate)}")
        if not isinstance(to_currency_rate, (int, float)) or to_currency_rate <= 0:
            logger.error("汇率无效")
            return None

        wallet_id = cls.wallet_list_page.get_currency_data(http_request, from_currency)['id']
        payee_id = cls.get_payee_address(http_request, to_currency)
        logger.info(f"收款方ID: {payee_id}")
        logger.info(f"钱包ID: {wallet_id}")

        if payee_id is None:
            logger.error("收款人ID获取失败")
            return None

        to_currency_amount = amount * to_currency_rate
        data = {
            "to_currency_rate": to_currency_rate,
            "to_currency_amount": to_currency_amount,
            "amount": amount,
            "payee_id": payee_id,
            "wallet_id": wallet_id,
            "memo": memo,
            "attachments": []
        }
        logger.info(f"提现参数: {data}")
        return data

    @classmethod
    def create_pay_out(cls,variables, http_request,test_case_name,from_currency,to_currency, amount,memo):
        """
        创建提现
        :param http_request:
        :param test_case_name:
        :param from_currency:
        :param to_currency:
        :param amount:
        :param memo:
        :return:
        """
        data = cls.pay_out_parameter(http_request,from_currency,to_currency, amount,memo)
        if data is None:
            return None
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables=variables,
            error_msg="创建提现失败")

    @classmethod
    def pay_out_fee(cls,http_request,from_currency,to_currency, amount):

        #获取ID
        id  = cls.get_payee_address(http_request,to_currency)
        print(f'收款方ID:{id}')
        #获取虚拟币的计算位和展示位
        data = cls.config._get_crypto_value(from_currency,['decimal_places','decimal_calculate_places'])
        decimal_places = float(data[0])#虚拟币的展示位
        decimal_calculate_places = float(data[1]) #虚拟币的计算位
        print(f'虚拟币的展示位:{decimal_places},虚拟币的计算位:{decimal_calculate_places}')
        result = cls.get_country_rate_data(http_request,from_currency,id)
        if result is None:
            return None

        rate_fee, per_count, prorate,network_per_fee,network_prorate_fee = result
        # rate_fee = cls.decimals.custom_round(rate_fee,decimal_calculate_places)
        # per_count = cls.decimals.custom_round(per_count,decimal_calculate_places)
        # prorate = cls.decimals.custom_round(prorate,decimal_calculate_places)
        # network_per_fee = cls.decimals.custom_round(network_per_fee,decimal_calculate_places)
        # network_prorate_fee = cls.decimals.custom_round(network_prorate_fee,decimal_calculate_places)





        fei = cls.get_rate_data(http_request, from_currency, to_currency)
        to_currency_amount = amount * fei

        _out_fee = prorate * amount + rate_fee * per_count + network_prorate_fee * amount + network_per_fee * rate_fee
        pay_out_fee = cls.decimals.custom_round(_out_fee,decimal_places)
        print(pay_out_fee)
        return pay_out_fee


if __name__ == '__main__':
        http_request = HttpRequest()
        pay_out = PayOut()
        to_currency = 'BWP'
        from_currency = 'USDT'
        amount = '160'
        memo = 'gift'
        pay_out_fee = pay_out.pay_out_parameter(http_request,from_currency, to_currency, amount,memo)


