import Common.logger as logger
logger = logger.logger



class GetCommonData:
    sheet_name = "Common"


    @classmethod
    def get_country_info_data(cls, http_request, test_case_name):
        """
        获取国家信息
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 国家信息
        """
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name)
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


    @classmethod
    def get_data_for_country(cls, http_request, test_case_name, country):
        """
        获取国家详情列表
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 部门列表
        """
        pin_data= 'business_type=reap_card'
        try:
            result = http_request._send_request(cls.sheet_name,
                                                test_case_name,
                                                jsonpath_expr=f"$.data[?(@.country_name='{country}')]",
                                                ping_data=pin_data)
            if result is None or len(result) != 4:
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                # print(response.text)
                logger.info(f'国家信息:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("获取数据，无响应返回")
                return None, None, None, None
        except Exception as e:
            logger.error(f"失败: {e}")
            raise e


    @classmethod
    def get_department_data(cls, http_request, test_case_name,department_name):
        """
        获取部门列表
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 部门列表
        """
        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                jsonpath_expr=f'$..children[?(@.name == "{department_name}")]')

            if result is None or len(result) != 4:
                logger.error("转账请求返回结果格式不正确")
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                # print(response.text)
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id

            else:
                logger.error("转账请求失败，无响应返回")
                return None, None, None, None

        except Exception as e:
            logger.error(f"失败: {e}")
            raise e

    @classmethod
    def get_user_id(cls, http_request, test_case_name,user_name):
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name, ping_data='page=1&take=10&name=',
                                                jsonpath_expr=f'$.data.data[?(@.first_name == \'{user_name}\')]')
            if result is None or len(result) != 4:
                logger.error("转账请求返回结果格式不正确")
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result

            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id

            else:
                logger.error("转账请求失败，无响应返回")
                return None, None, None, None
        except Exception as e:
            logger.error(f"失败: {e}")
            raise e
