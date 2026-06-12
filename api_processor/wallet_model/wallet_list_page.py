from Common.simple_request import HttpRequest
from Common.read_and_save_tool import ConfigTools
import Common.logger as logger
logger = logger.logger

class WalletListPage:
    sheet_name = 'Wallte_page'
    config = ConfigTools()

    @classmethod
    def get_wallet_list(cls,test_case_name,http_request):
        """
        获取钱包列表
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :return: 钱包列表
        """

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            nested_keys =['data','list'],
            error_msg="获取钱包列表失败")
    @classmethod
    def get_currency_data(cls,http_request,from_currency):
        """
        获取币种数据
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :param currency: 要获取的币种
        :return: 币种数据:id,currency,amount,price,total_balance,percent,
        """
        response, extracted_parameters, assert_code, case_id = cls.get_wallet_list('钱包-获取钱包列表',http_request)
        # print( len(extracted_parameters))
        if extracted_parameters is None:
            logger.error("获取钱包列表失败，无法获取币种数据")
            return None
        else:
            for i in extracted_parameters:
                # print(i)
                if i['currency'] == from_currency:
                    logger.info(f"获取币种数据成功，币种数据为：{i}")
                    return i

            # 循环结束后仍未找到匹配项
            logger.error(f"未找到币种为{from_currency}的数据")
            return None


    @classmethod
    def _get_currency_data(cls, http_request, to_currency):
        """
        获取币种数据
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :param currency: 要获取的币种
        :return: 币种数据:id,currency,amount,price,total_balance,percent,
        """
        response, extracted_parameters, assert_code, case_id = cls.get_wallet_list('钱包-获取钱包列表', http_request)
        # print( len(extracted_parameters))
        if extracted_parameters is None:
            logger.error("获取钱包列表失败，无法获取币种数据")
            return None
        else:
            for i in extracted_parameters:
                # print(i)
                if i['currency'] == to_currency:
                    logger.info(f"获取币种数据成功，币种数据为：{i}")
                    return i

            # 循环结束后仍未找到匹配项
            logger.error(f"未找到币种为{to_currency}的数据")
            return None
    @classmethod
    def get_chain_list(cls, test_case_name, http_request):
        """
        获取链数据
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :return: 链数据:chain_id,chain_name,symbol
        """
        chain_name_list =[]
        response, extracted_parameters, assert_code, case_id = http_request.execute_case(
                                                                sheet_name=cls.sheet_name,
                                                                test_case_name=test_case_name,
                                                                nested_keys=['data', 'data'],
                                                                error_msg="获取链列表失败")
        for i in extracted_parameters:
            chain_name_list.append(i['chain_name'])
        cls.config.save_value('CHAIN_NAME', 'chain_name', chain_name_list)
        # print("获取链列表", extracted_parameters)
        if extracted_parameters is not None:
            return response, extracted_parameters, assert_code, case_id
        else:
            logger.error("获取链列表请求失败，无响应返回")
            return response, None, assert_code, case_id


    @classmethod
    def get_chain_data(cls, http_request, chain_name):
        """
        获取链数据
        :param http_request: HttpRequest实例
        :param chain_name: 要获取的链名称
        :return: 链数据:chain_id,chain_name,symbol
        """
        response, extracted_parameters, assert_code, case_id = cls.get_chain_list(
            '钱包-获取支持的链列表', http_request)
        if extracted_parameters is None:
            logger.error("获取链列表失败，无法获取链数据")
            return None

        # 遍历所有链数据查找匹配项
        for i in extracted_parameters:
            if isinstance(i, dict) and i.get('chain_name') == chain_name:
                logger.info(f"获取链数据成功，链数据为：{i}")
                return i

        # 只有遍历完所有元素都没找到才返回None
        logger.error(f"未找到链名称为{chain_name}的数据")
        return None


    # dropdown_transaction_type
    @classmethod
    def get_dropdown_for_currency_type(cls, test_case_name,http_request,currency_type):
        """
        获取交易类型数据
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :return:
        """

        data = {'currency_type':currency_type}


        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            dict_data=data,
            nested_keys=['data'],
            error_msg="获取交易类型数据失败")
    @classmethod
    def save_all_currency_data(cls,result,currency_type):
        """
        获取所有加密货币数据
        :param http_request: HttpRequest实例
        :return:
        """
        data_list = []
        response, extracted_parameters, assert_code, case_id = result
        if extracted_parameters is not None:
            for i in extracted_parameters:
                data_list.append(i['currency'])

        cls.config.save_value(section=f'{currency_type}_data', key=f'{currency_type}_list',
                              value=data_list)


    #保存获取的参数
    @classmethod
    def save_dropdown_for_currency_type(cls, result,currency_type,currency):
        """
        保存获取的加密货币数据
        :param currency_type: 要获取的币种类型
        :return:
        """
        ditc_data = {}
        response, extracted_parameters, assert_code, case_id = result
        if extracted_parameters is not None:
            for i in extracted_parameters:
                if i['currency'] == currency:
                    if currency_type == 'crypto':
                        ditc_data['currency'] = i['currency']
                        ditc_data['decimal_places'] = i['decimal_places']
                        ditc_data['decimal_calculate_places'] = i['decimal_calculate_places']
                        ditc_data['min_increment'] = float(i['min_increment'])
                        ditc_data['chain'] = i['chain']
                    elif currency_type == 'fiat':
                        ditc_data['currency'] = i['currency']
                        ditc_data['decimal_places'] = i['decimal_places']
                        ditc_data['decimal_calculate_places'] = i['decimal_calculate_places']
                        ditc_data['min_increment'] = float(i['min_increment'])


        cls.config.save_value(section=f'{currency_type}_data', key=f'{currency_type}_{currency}_dict',
                                value=ditc_data)



















    def get_dropdown_for_transaction_type(cls, test_case_name, http_request,transaction_type):
        """
        获取加密货币数据
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :return:
        """
        send_dict={}
        data = {
            'transaction_type': transaction_type
        }

        response, extracted_parameters, assert_code, case_id = http_request.execute_case(
                                                                            sheet_name=cls.sheet_name,
                                                                            test_case_name=test_case_name,
                                                                            dict_data=data,
                                                                            nested_keys=['data'],
                                                                            error_msg="获取加密货币数据失败")
        # print(extracted_parameters)
        #存起来方便后续使用
        for i in extracted_parameters:
            send_dict[i['remarks']] = {'country':i['country'],'currency':i['currency'],'min_limit':float(i['min_limit']),'max_limit':float(i['max_limit'])}
        cls.config.save_value(section=f'{transaction_type}_data',key=f'{transaction_type}_dict',value=send_dict)
        if extracted_parameters is not None:
            return response, extracted_parameters, assert_code, case_id
        else:
            logger.error("获取payout列表请求失败，无响应返回")
            return response, None, assert_code, case_id




    @classmethod
    def get_dropdown_for_transaction_type_and_country(cls, test_case_name, http_request,transaction_type,country):
        """
        获取加密货币数据
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :return:
        """
        data = {
            'transaction_type': transaction_type,
            'country': country
        }

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            dict_data=data,
            nested_keys=['data'],
            error_msg="获取交易类型数据失败")
