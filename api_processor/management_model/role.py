import Common.logger as logger
import ast
logger = logger.logger
from Common.read_and_save_tool import ConfigTools



class RoleManagement:
    sheet_name = 'management_page'
    create_name = 'test_001_name'
    put_name = 'test_002_name'
    config = ConfigTools()
    menu_ids = config.get_menu_ids()




    def get_create_data(self):
        """
        获取配置id
        :return:
        """


        if self.menu_ids is None:
            self.menu_ids = []  # 或根据业务逻辑赋予默认值
        payload = {
            "role_name": self.create_name,
            "approval_limit": -1,
            "menu_ids": self.menu_ids
        }
        print( type(payload))
        return  payload
    @classmethod
    def create_role(cls,http_request,test_case_name):
        """

        创建角色
        :param http_request:
        :param test_case_name:
        :return:
        """
        payload = cls.get_create_data(cls)

        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                variables = payload)

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
    def get_role_data(cls,http_request,test_case_name):
        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                jsonpath_expr=f'$.data[?(@.name=="{cls.create_name}")].id')

            if result is None or len(result) != 4:
                logger.error("转账请求返回结果格式不正确")
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            print(extracted_parameters)
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id

            else:
                logger.error("转账请求失败，无响应返回")
                return None, None, None, None

        except Exception as e:
            logger.error(f"失败: {e}")
            raise e
    def get_role_id(self,http_request):
        result = self.get_role_data(http_request, '管理-获取角色列表')
        response, extracted_parameters, assert_code, case_id = result
        return extracted_parameters

    def get_update_role_data(self,http_request):
        """
        pin 更新的数据
        :param http_request:
        :return:
        """
        role_id = self.get_role_id(self,http_request)

        payload = {
            "role_name": self.put_name,
            "approval_limit": -1,
            "menu_ids": self.menu_ids,
            "role_id": role_id
        }
        print(type(payload))
        return payload
    @classmethod
    def put_role(cls,http_request,test_case_name):
        payload = cls.get_update_role_data(cls, http_request)

        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                variables= payload)

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
    def delete_role(cls,http_request,test_case_name):
        role_id = cls.get_role_id(cls,http_request)
        payload = {
            "id": role_id
        }

        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                data= payload)

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




