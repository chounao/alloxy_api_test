import Common.logger as logger
logger = logger.logger

class Departments:
    sheet_name = 'management_page'

    create_name = 'test_001_name'
    put_name = 'test_002_name'

    @classmethod
    def get_department_data(cls,http_request,test_case_name):
        """
        获取部门列表
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return:
        """

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            jsonpath_expr='$.data[0].department_id'
        )

    @classmethod
    def get_department_id_for_name(cls,http_request,test_case_name,department_name):
        """
        获取部门id
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :param department_name: 部门名称
        :return: 部门id
        """

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            jsonpath_expr=f'$..children[?(@.name == "{department_name}")].department_id'
        )
    def get_department_root_id(self,http_request):
        """

        获取rootid
        :param http_request:
        :return:
        """
        result = self.get_department_data(http_request, '管理-获取部门列表')
        response, extracted_parameters, assert_code, case_id = result
        return extracted_parameters



    def get_department_id(self,http_request,department_name):
        """
        获取创建的id
        :param http_request:
        :param department_name:
        :return:
        """
        result = self.get_department_id_for_name(http_request, '管理-获取部门列表',department_name)
        response, extracted_parameters, assert_code, case_id = result
        return extracted_parameters

    @classmethod
    def create_department(cls,http_request,test_case_name):
        """
        创建部门
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 部门id
        """
        data = {
            "name": cls.create_name,
            "parent_department_id": cls.get_department_root_id(cls,http_request)
        }

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables= data
        )



    @classmethod
    def put_department(cls,http_request,test_case_name):
        """
        修改部门
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 部门id
        """
        data = {
            "name": cls.put_name,
            "parent_department_id": cls.get_department_root_id(cls,http_request),
            "department_id": cls.get_department_id( cls,http_request,cls.create_name)
        }

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables= data
        )

    @classmethod
    def delete_department(cls,http_request,test_case_name):
        """
        删除部门
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 部门id
        """
        body = {'id':cls.get_department_id( cls,http_request,cls.put_name)}
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            replace_data= body
        )














