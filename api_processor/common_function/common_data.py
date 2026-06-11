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
        return  http_request.execute_case(
                                            sheet_name=cls.sheet_name,
                                            test_case_name=test_case_name,
                                            error_msg="获取国家信息失败")


    @classmethod
    def get_data_for_country(cls, http_request, test_case_name, country):
        """
        获取国家详情列表
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 部门列表
        """
        pin_data= 'business_type=reap_card'
        return http_request.execute_case(
                                        cls.sheet_name,
                                        test_case_name,
                                        jsonpath_expr=f"$.data[?(@.country_name='{country}')]",
                                        ping_data=pin_data,
                                        error_msg="获取国家详情列表失败")


    @classmethod
    def get_department_data(cls, http_request, test_case_name,department_name):
        """
        获取部门列表
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 部门列表
        """
        return http_request.execute_case(
                                        cls.sheet_name,
                                        test_case_name,
                                        jsonpath_expr=f'$..children[?(@.name == "{department_name}")]',
                                        error_msg="获取国家详情列表失败")

    @classmethod
    def get_user_id(cls, http_request, test_case_name,user_name):
        return http_request.execute_case(
                                    cls.sheet_name,
                                    test_case_name,
                                    ping_data='page=1&take=10&name=',
                                    jsonpath_expr=f'$.data.data[?(@.first_name == \'{user_name}\')]',
                                    error_msg="获取用户ID失败")



