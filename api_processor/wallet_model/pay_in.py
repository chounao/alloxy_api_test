import Common.logger as logger
from api_processor.wallet_model.wallet_list_page import WalletListPage

logger = logger.logger

class PayIn:
    sheet_name = 'Wallte_page'
    wallet_list_page = WalletListPage()





    @classmethod
    def get_country_info(cls,http_request,test_case_name):
        """
        获取国家信息
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 国家信息
        """

        data = {
            'business_type': 'yellowcard_payin',
        }


        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            dict_data=data,
            nested_keys=['data'])


    @classmethod
    def get_fiat_in_fee(cls,http_request,test_case_name):
        """
        获取法币到 crypto 的手续费
        :param http_request:
        :param test_case_name:
        :return:
        """
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name)



    @classmethod
    def get_pay_in_fee(cls,http_request,test_case_name,from_currency, to_currency):
        """
        获pay_in的手续费
        :param http_request:
        :param test_case_name:
        :return:
        """
        data = {
            'from_currency': from_currency,
            'to_currency': to_currency,
        }

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            dict_data=data,
            nested_keys=['data'])


    @classmethod
    def _pay_in_data(cls,http_request, from_currency, to_currency):
        try:
            response, extracted_parameters, assert_code, case_id = cls.get_pay_in_fee(http_request, '钱包-获取汇率',from_currency, to_currency)

            return extracted_parameters
        except Exception:
            return None

    @classmethod
    def pay_in_parameter(cls, http_request, from_currency, to_currency, amount):
        """
        获取payin参数
        :param http_request: HTTP 请求实例
        :return:
        """
        send_amount = 1.0 if amount == 0.00 else amount or 1.0

        try:
            extracted_parameters = cls._pay_in_data(http_request, from_currency, to_currency)

            # 增加参数有效性检查
            if not extracted_parameters:
                logger.error(f"获取支付参数失败: extracted_parameters is None")
                return None

            # 安全访问嵌套字典
            data = extracted_parameters.get('data')
            if not data:
                logger.error(f"获取支付参数失败: data字段不存在")
                return None

            country = data.get('locale')
            if not country:
                logger.error(f"获取支付参数失败: locale字段不存在")
                return None

            variables = {
                'country': country,
                'from_currency': from_currency,
                'to_currency': to_currency,
                'amount': send_amount,
            }
            logger.info(f"成功获取支付参数: {variables},{type(variables)}")
            return variables

        except KeyError as e:
            logger.error(f"参数提取失败，缺少必要字段: {e}")
            return None
        except Exception as e:
            logger.error(f"获取支付参数时发生未知错误: {e}")
            return None

    @classmethod
    def pay_in_submit(cls,test_case_name,http_request, from_currency, to_currency,amount):
        variables = cls.pay_in_parameter(http_request,from_currency, to_currency, amount)

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables = variables)