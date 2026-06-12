import json
import string
import ast
import pytest
from Common.read_and_save_tool import ConfigTools
import Common.logger as logger
from Common.simple_request import HttpRequest
from api_processor.wallet_model.wallet_list_page import WalletListPage
import random
logger = logger.logger


class Payee:
    sheet_name = 'Wallte_page'
    wallet_list_page = WalletListPage()
    config_manager = ConfigTools()


    # 获取币种收款方数据
    @classmethod
    def get_crypto_payee_data(cls, test_case_name, http_request,body,page=1, take=20, max_pages=None):
        """
        获取币种收款方数据
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :param from_currency: 要获取的币种
        :param chain_name: 要获取的链名称
        :return:
        """
        logger.info(f'提币地址列表')
        all_extracted_parameters = []
        current_page = page

        while True:
            data = {
                'page': current_page,
                'take': take,
            }

            # 明确判断 body 是否有效再合并
            if isinstance(body, dict):
                data.update(body)


                response, extracted_parameters, assert_code, case_id = http_request.execute_case(
                                                                        sheet_name=cls.sheet_name,
                                                                        test_case_name=test_case_name,
                                                                                        dict_data=data,
                                                                                    nested_keys=['data'],
                                                                            error_msg="获取币种收款方数据失败")

                # 检查是否有数据返回
                if not extracted_parameters:
                    logger.info(f"[{test_case_name}] 第{current_page}页无数据，停止查询")
                    break

                # 合并当前页数据
                all_extracted_parameters.extend(extracted_parameters)

                # 检查是否还有下一页
                total_count = response.get('data', {}).get('count', 0)
                current_total = current_page * take

                # 如果已经达到最大页数限制或没有更多数据，则停止
                if (max_pages and current_page >= max_pages) or current_total >= total_count:
                    logger.info(f"[{test_case_name}] 已达到最大页数限制或无更多数据")
                    break

                current_page += 1

        # 返回合并后的所有数据
        return response, all_extracted_parameters, assert_code, case_id
    @classmethod
    def get_payee_data(cls, http_request, payee_name):
        response, extracted_parameters, assert_code, case_id  = cls.get_crypto_payee_data('钱包-获取加密收款地址列表', http_request, body={'payee_name': payee_name})

        total = extracted_parameters['total']

        # 使用get方法和默认值处理
        payee_list = extracted_parameters.get('list', [])
        if not payee_list:
            return None  # 或抛出自定义异常

        id = payee_list[0].get('id')
        if id is None:
            raise ValueError("收款人数据缺少'id'字段")
        return total, id

    #添加收款方——添加地址薄
    @classmethod
    def add_payee(cls,test_case_name, http_request, payee_name, currency, chain_name):
        """
        添加收款方
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :param payee_name: 收款方名称
        :param currency: 币种
        :param chain_name: 链名称
        :return:
        """
        logger.info(f'添加收款方：{payee_name}，币种：{currency}，链名称：{chain_name}')
        #添加空值检查
        chain_data = cls.wallet_list_page.get_chain_data(http_request, chain_name)
        if chain_data is None:
            raise ValueError(f"未找到链名称 '{chain_name}' 对应的链数据")
        chain_id = chain_data['chain_id']
        #随机生成钱包地址（字母+数字8位）
        wallet_address = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        variables = {
         "payee_name":payee_name,
         "currency":currency,
         "chain_id":chain_id,
         "wallet_address": wallet_address

        }
        logger.info(f'添加收款方请求参数：{variables}')

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables= variables,
            error_msg="添加收款方失败")
    @classmethod
    def create_payee(cls,http_request,payee_name,currency,chain_name):
        result = cls.add_payee('钱包-创建加密收款地址', http_request, payee_name, currency, chain_name)
        response, extracted_parameters, assert_code, case_id = result
        total, id = cls.get_payee_data(http_request, payee_name)
        if response is not None:
            return id
        else:
            logger.error("添加收款方请求失败，无响应返回")
            return None

    # 删除收款方
    @classmethod
    def delete_payee(cls, test_case_name, http_request, payee_name,currency,chain_name):
        """
        删除收款方
        :param test_case_name: 测试用例名称
        :param http_request: HttpRequest实例
        :param payee_name: 收款方名称
        :param currency: 币种
        :param chain_name: 链名称
        :return:
        """
        logger.info(f'删除收款方：{payee_name}')
        id = cls.create_payee(http_request, payee_name, currency, chain_name)

        if id is None:
            logger.error(f'收款方：{payee_name}不存在')
            return None, None, None, None

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            replace_data=id,
            error_msg="删除收款方失败")
    #收款银行账户查询接口
    @classmethod
    def get_payee_bank_account(cls, test_case_name, http_request,payee_name):
        """

        :param test_case_name:
        :param http_request:
        :param payee_name:
        :return:
        """
        data = {
            'page': 1,
            'take': 200,
            'payee_name': payee_name
        }

        logger.info(f'收款银行账户列表查询参数：{data}')

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            dict_data=data,
            nested_keys=['data'],
            error_msg="收款银行账户列表查询失败")
    @classmethod
    def get_all_country_data(cls, http_request, test_case_name):
        """
        获取所有支持的国家
        :param test_case_name:
        :param http_request:
        :return:
        """
        country_list = []
        response, extracted_parameters, assert_code, case_id =http_request.execute_case(
                                                                                        sheet_name=cls.sheet_name,
                                                                                        test_case_name=test_case_name,
                                                                                        nested_keys=['data'],
                                                                                        error_msg="获取所有支持的国家失败")
        for i in extracted_parameters:
            data = i['iso2']
            country_list.append(data)
        if response is not None:
            return response, country_list, assert_code, case_id
        else:
            logger.error("获取所有支持的国家失败，无响应返回")
            return response, None, assert_code, case_id
    # 获取币种支持的国家
    @classmethod
    def get_foreign_currency_supported_countries(cls, http_request, test_case_name, currency, country_code):
        """
        获取币种支持的国家
        :param test_case_name:
        :param http_request:
        :param currency:
        :param country_code:
        :return:
        """
        body = {
            'network': 'network:local',
            'currency': currency,
            'country_code': country_code
        }

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables=body,
            nested_keys=['data'],
            error_msg="获取币种支持的国家失败")
    @classmethod
    def get_random_country_code(cls, http_request, currency, country_code):
        """
        获取随机国家代码
        :return:
        """
        data_list = []
        result = cls.get_foreign_currency_supported_countries(http_request, '查询币种支持的银行国家', currency,
                                                              country_code)
        response, extracted_parameters, assert_code, case_id = result

        if not extracted_parameters:
            logger.warning(
                f"extracted_parameters is empty or None for currency: {currency}, country_code: {country_code}")
            return None

        data_list = [i['name'] for i in extracted_parameters]


        # 在列表随机选择一个国家
        if data_list != None:
            name = random.choice(data_list)

            return name
        else:
            return None
    #银行账户列表
    @classmethod
    def get_payee_bank_account_data(cls, http_request,payee_name):
        """

        :param test_case_name:
        :param http_request:
        :param payee_name:
        :return:
        """
        id_list = []
        result = cls.get_payee_bank_account('钱包-获取法币收款地址列表', http_request, payee_name)
        response, extracted_parameters, assert_code, case_id = result
        if response.status_code != 200:
            pytest.fail(f"获取收款方失败: {response.status_code}")
            return None, None
        total = extracted_parameters['total']

        # 使用get方法和默认值处理
        payee_list = extracted_parameters.get('list', [])
        for i in payee_list:
            if i['status'] == 'active':
                id_list.append(i['id'])

        # if not payee_list:
        #     return None  # 或抛出自定义异常
        #
        # id = payee_list[0].get('id')
        # if id is None:
        #     raise ValueError("收款人数据缺少'id'字段")
        return total, id_list
    def get_payee_account_data(cls, http_request,payee_name):
        """

        :param test_case_name:
        :param http_request:
        :param payee_name:
        :return:
        """
        id_list = []
        result = cls.get_payee_bank_account('钱包-查看银行信息详情', http_request, payee_name)
        response, extracted_parameters, assert_code, case_id = result
        if response.status_code != 200:
            pytest.fail(f"获取收款方失败: {response.status_code}")
            return None, None
        total = extracted_parameters['total']

        # 使用get方法和默认值处理
        payee_list = extracted_parameters.get('list', [])
        for i in payee_list:
            if i['status'] == 'active':
                id_list.append(i['id'])

        # if not payee_list:
        #     return None  # 或抛出自定义异常
        #
        # id = payee_list[0].get('id')
        # if id is None:
        #     raise ValueError("收款人数据缺少'id'字段")
        return total, id_list

    #银行账户的信息
    @classmethod
    def send_body(cls, payee_type, payment_data, http_request):
        logger.info("开始发送请求，payee_type: %s, payment_data: %s", payee_type, payment_data)
        # 初始化本地变量替代类属性
        cls.country_code = ''
        cls.currency = ''
        cls.bank_name = ''
        payment_type = payment_data[0]
        input_currency = payment_data[1]

        section = 'test_data'

        # 缓存常用配置项防止重复解析
        config_get = cls.config_manager.get_value
        banks = ast.literal_eval(config_get(section, 'banks'))
        cities = ast.literal_eval(config_get(section, 'cities'))
        states = ast.literal_eval(config_get(section, 'states'))
        streets = ast.literal_eval(config_get(section, 'streets'))
        first_names = ast.literal_eval(config_get(section, 'first_names'))
        last_names = ast.literal_eval(config_get(section, 'last_names'))

        # 随机选择银行及账号
        selected_bank = random.choice(banks)
        account_number = ''.join(str(random.randint(0, 9)) for _ in range(16))

        # 国家邮编规则映射表
        postcode_formats = {
            'US': lambda: f"{random.randint(10000, 99999)}",
            'UK': lambda: f"{random.choice(string.ascii_uppercase)}{random.randint(1, 9)} "
                          f"{random.randint(1, 9)}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}",
            'CA': lambda: f"{random.choice(string.ascii_uppercase)}{random.randint(1, 9)}"
                          f"{random.choice(string.ascii_uppercase)} {random.randint(1, 9)}"
                          f"{random.choice(string.ascii_uppercase)}{random.randint(1, 9)}",
            'AU': lambda: f"{random.randint(1000, 9999)}",
            'SG': lambda: f"{random.randint(100000, 999999)}",
        }

        # 获取随机国家码
        _country_code = random.choice(
            ast.literal_eval(config_get('country_code_list', 'country_list'))
        )

        supported_currencies = ['SGD', 'AED', 'GBP', 'CAD']

        # data = cls.get_random_country_code(http_request, input_currency, _country_code)

        if payment_type == 'international':
            cls.currency = 'USD'
            cls.country_code = _country_code
        elif payment_type == 'local':
            # if input_currency in supported_currencies:
            #     cls.currency = input_currency
            #     cls.country_code = input_currency[:2]
            # else:
            #     cls.currency = input_currency
            #     cls.country_code = _country_code
            if input_currency :

                cls.currency = input_currency
                if cls.currency == 'EUR':
                    cls.country_code = 'SE'
                else:
                    cls.country_code = input_currency[:2]


        # 地址相关字段构建
        postcode_func = postcode_formats.get(_country_code, lambda: f"{random.randint(100000, 999999)}")
        street_number = random.randint(1, 999)

        # 名字生成
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        bank_name = cls.get_random_country_code(http_request, cls.currency, cls.country_code)

        # 设置默认银行名称
        final_bank_name = selected_bank['name']  # 默认使用选定的银行名称
        # 如果获取到了bank_name且是本地支付类型，则使用获取到的bank_name
        if bank_name is not None and payment_type == 'local':
            final_bank_name = bank_name
            logger.info('bank_name已经更新: %s', bank_name)
        # 构建基础 body 字典
        body = {
            "type": "bank",
            "payment_type": payment_type,
            "currency": cls.currency,
            "bank_address": {
                "country": cls.country_code
            },
            "bank_name": final_bank_name,
            "account_no_iban": account_number,
            "bic_swift": selected_bank['code'],
            "payee_type": payee_type,
            "relation": "GRAND_FATHER",
            "payee_address": {
                "postCode": postcode_func(),
                "country": cls.country_code,
                "state": random.choice(states),
                "city": random.choice(cities),
                "line1": f"{random.choice(streets)} {street_number}"
            },
            "first_name": first_name
        }

        # 添加个人姓名字段
        if payee_type == 'personal':
            body["last_name"] = last_name
            # 在设置body之前先获取bank_name

        # 如果是本地支付并且货币支持，则添加银行账户信息 如果bank_name为None，则使用默认银行名称,如果bank_name不为空则使用银行名称
        try:
            if bank_name is not None and cls.bank_name == "":
                if payment_type == 'local' :

                    print('-------',bank_name)
                    # name = {
                    #     "bank_name": bank_name,
                    # }
                    #判断bank_name如果为空，则使用默认银行名称，如果bank_name返回的参数不为空则更新bank_name

                    cls.bank_name = bank_name
                    logger.info('bank_name已经更新: %s', bank_name)
                else:
                    cls.bank_name = selected_bank['name']
                    logger.warning('bank_name is None or empty, using default bank_name')
        except Exception as e:
            logger.error(f"获取随机国家代码失败: {e}")
            raise e





        logger.info(f"创建收款方参数: {body}")
        return body

    @classmethod
    def create_payee_bank_account(cls, http_request,test_case_name,body):
        """
        创建收款方银行账户
        :param test_case_name:
        :param body : 收款方银行账户信息international，
                       local:{ currency :SGD,HKD,BWP,KES,MWK,NGN,RWF,ZAR,TZS,UGX,ZMW,
                            currencys:AED,GBP,CAD,EUR}
                    loacl :currency:'SGD,
                            "bank_address": {
                            "country": "SG"
                        }
        :param http_request:
        :param payee_name:
        :return:
        """

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables=body,
            error_msg="创建收款方银行账户失败")



    #查看详情
    @classmethod
    def get_payee_bank_account_details(cls, test_case_name, http_request, payee_id):
        """
        获取收款方银行账户详情
        :param test_case_name:
        :param http_request:
        :param payee_id:
        :return:
        """
        # total, id = cls.get_payee_bank_account_data( http_request, payee_name = '')
        # payee_id = random.choice(id)
        data = {
            'id': payee_id
        }

        response, extracted_parameters, assert_code, case_id = http_request.execute_case(
                                                                                            sheet_name=cls.sheet_name,
                                                                                            test_case_name=test_case_name,
                                                                                            dict_data=data,
                                                                                            nested_keys=['data', 'list', 0],
                                                                                            error_msg="获取收款方银行账户详情失败")

        keys_to_remove = ['created_at','update_at','remarks','account_id','bank_code','branch_name',
                          'branch_code','routing_type1','routing_number1','routing_type2','routing_number2'
                          ,'status','label','routing_number2','payees_name']
        for key in keys_to_remove:
            extracted_parameters.pop(key, None)
        extracted_parameters['type'] = 'bank'
        print(
            "获取收款方银行账户详情参数: %s",
            json.dumps(extracted_parameters)
        )
        if response is not None:
            return response, extracted_parameters, assert_code, case_id
        else:
            logger.error("获取收款方银行账户详情失败，无响应返回")
            return response, None, assert_code, case_id


    #编辑操作
    @classmethod
    def update_payee_bank_account(cls, test_case_name, http_request, body):
        """
        编辑收款方银行账户
        :param test_case_name:
        :param http_request:
        :param payee_id:
        :param body:
        :return:
        """
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables=body,
            nested_keys=['data'],
            error_msg="编辑收款方银行账户失败")

    #删除银行账户
    @classmethod
    def delete_payee_bank_account(cls, test_case_name, http_request, payee_id):
        """

        :param test_case_name:
        :param http_request:
        :param payee_id:
        :return:
        """
        data = {
            'id': payee_id
        }
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            replace_data=data,
            error_msg="删除收款方银行账户失败")









if __name__ == '__main__':

    payee_type = ['personal', 'business']
    currency_mapping = {'international': ['USD'],
          'local': ['SGD', 'HKD', 'BWP', 'KES', 'MWK', 'NGN', 'RWF', 'ZAR', 'TZS', 'UGX', 'ZMW', 'AED', 'GBP', 'CAD',
                    'EUR', 'AED', 'GBP', 'CAD', 'EUR']}
    payee = Payee()
    for  i in payee_type:
        for key,value in currency_mapping.items():
            for currency in value:
                payee.send_body(i, [key, currency])














































