import Common.logger as logger
logger = logger.logger

class CardTransaction:
    sheet_name = "Card_page"


    @classmethod
    def get_card_transaction_data(cls, http_request, test_case_name,transaction_type, status, transaction_sub_type):
        """
        获取卡片交易列表
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 卡片交易列表
        """
        # page = 1
        # params_data = {
        #     'page': page,
        #     'take': 100
        #
        # }
        # if transaction_sub_type:
        #     params_data['transaction_sub_type'] = transaction_sub_type
        # if transaction_type:
        #     params_data['transaction_type'] = transaction_type
        # if status:
        #     params_data['status'] = status

        params_data = f'page=1&take=20&transaction_type={transaction_type}&status={status}&transaction_sub_type={transaction_sub_type}'


        try:
            result = http_request._send_request(cls.sheet_name, test_case_name,ping_data=params_data)
            if result is None or len(result) != 4:
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("获取数据，无响应返回")
        except Exception as e:
            logger.error(f"失败: {e}")
            raise e


