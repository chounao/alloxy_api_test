import Common.logger as logger
from api_processor.wallet_model.wallet_list_page import WalletListPage

logger = logger.logger
class Recharge:
    sheet_name = 'Wallte_page'
    wallet_list_page = WalletListPage()


    def chain_deposit(cls, test_case_name, http_request, currency,chain_name):
        """
        充值
        :param http_request: HttpRequest实例
        :param currency: 币种
        :param chain_name: 链名称
        :return: 充值结果
        """
        logger.info(f"Processing chain: {chain_name}, currency: {currency}")
        chain_data = cls.wallet_list_page.get_chain_data(http_request, chain_name)
        if chain_data is None:
            raise ValueError(f"未找到链名称 '{chain_name}' 对应的链数据")
        chain_id = chain_data['chain_id']
        data = {
            'page': 1,
            'take': 100,
            'currency': currency,
            'chain_ids': chain_id,

        }

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            dict_data=data,
            nested_keys=['data', 'adress'])

