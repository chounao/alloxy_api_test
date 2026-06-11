import Common.logger as logger
from api_processor.wallet_model.wallet_list_page import WalletListPage

logger = logger.logger
class Recharge:
    sheet_name = 'Wallte_page'
    wallet_list_page = WalletListPage()


    def chain_deposit(cls, test_case_name, http_request, currency,chain_name):
        logger.info(f"Processing chain: {chain_name}, currency: {currency}")
        chain_data = cls.wallet_list_page.get_chain_data(http_request, chain_name)
        if chain_data is None:
            raise ValueError(f"未找到链名称 '{chain_name}' 对应的链数据")
        chain_id = chain_data['chain_id']
        try:
            data = {
                'page': 1,
                'take': 100,
                'currency': currency,
                'chain_ids': chain_id,

            }
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                dict_data=data,
                nested_keys=['data', 'adress']
            )
            if result is None or len(result) != 4:
                logger.error("返回结果格式不正确")
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            print(extracted_parameters)
            if response is not None:
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("请求失败，无响应返回")
                return response, None, assert_code, case_id
        except Exception as e:
            logger.error(f"获取收款方失败: {e}")
            raise e
