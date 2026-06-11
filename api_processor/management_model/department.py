import Common.logger as logger
logger = logger.logger

class Departments:
    sheet_name = 'management_page'

    create_name = 'test_001_name'
    put_name = 'test_002_name'

    @classmethod
    def get_department_data(cls,http_request,test_case_name):
        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                jsonpath_expr='$.data[0].department_id')

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
    @classmethod
    def get_department_id_for_name(cls,http_request,test_case_name,department_name):
        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                jsonpath_expr=f'$..children[?(@.name == "{department_name}")].department_id')

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
        data = {
            "name": cls.create_name,
            "parent_department_id": cls.get_department_root_id(cls,http_request)
        }
        try:
            result = http_request._send_request(
                cls.sheet_name, test_case_name,variables= data)

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




    @classmethod
    def put_department(cls,http_request,test_case_name):
        data = {
            "name": cls.put_name,
            "parent_department_id": cls.get_department_root_id(cls,http_request),
            "department_id": cls.get_department_id( cls,http_request,cls.create_name)
        }
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name,variables= data)
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



    @classmethod
    def delete_department(cls,http_request,test_case_name):
        body = {'id':cls.get_department_id( cls,http_request,cls.put_name)}
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name,replace_data= body)

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















