import Common.logger as logger
logger = logger.logger
from Common.read_and_save_tool import ConfigTools
from faker import Faker
import random
import hashlib


class UserManagement:
    sheet_name = 'management_page'


    create_last_name = 'EDG'
    create_first_name = 'baby'
    PUT_last_name = 'UZI'
    phone = None
    email = None
    user_id = 'c3190d0c-4c2a-45a6-9ea2-26e45299c31b'
    config = ConfigTools()
    pass_word = config.get_login_data('PASSWORD')


    def get_id_for_name(self,http_request):
        result1= http_request._send_request(self.sheet_name,'管理-获取部门列表',
                                                  jsonpath_expr="$.data[0].children[?(@.name == 'test_001_name')].department_id")
        response, extracted_parameters, assert_code, case_id = result1
        department_id = extracted_parameters
        result2 = http_request._send_request(self.sheet_name,'管理-获取角色列表',
                                            jsonpath_expr="$.data[?(@.name == 'test_001_name')].id")
        response, extracted_parameters, assert_code, case_id = result2
        role_id = extracted_parameters
        # print(department_id, role_id)
        return department_id, role_id
    @classmethod
    def get_create_user_data(cls,http_request):
        department_id, role_id = cls.get_id_for_name(cls,http_request)

        fake = Faker('en_US')
        # cls.last_name = fake.last_name()
        # cls.first_name = fake.first_name()
        cls.email = fake.email()
        cls.phone = f"1{random.choice('3456789')}{''.join([str(random.randint(0, 9)) for _ in range(9)])}"

        payload = {
            "last_name": cls.create_last_name,
            "first_name": cls.create_first_name,
            "role_id": role_id,
            "department_id": department_id,
            "phone": cls.phone,
            "email": cls.email
        }
        return  payload
    @classmethod
    def create_user(cls,http_request,test_case_name):
        payload  = cls.get_create_user_data(http_request)
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name, variables= payload)
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
    def get_user_id(cls,http_request,test_case_name):
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name,ping_data='page=1&take=10&name=',
                jsonpath_expr=f'$.data.data[?(@.first_name == \'{cls.create_first_name}\')].id')
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

    @classmethod
    def update_user_info(cls, http_request,test_case_name):
        payload  = cls.get_create_user_data(http_request)
        response, extracted_parameters, assert_code, case_id = cls.get_user_id(http_request, '管理-获取成员列表')
        payload['member_id'] = extracted_parameters
        payload['last_name'] = cls.PUT_last_name
        print( payload)
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name, variables= payload)
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
    def reset_password (cls, http_request, test_case_name):
        md5 = hashlib.md5()
        md5.update(cls.pass_word.encode('utf-8'))
        response, extracted_parameters, assert_code, case_id = cls.get_user_id(http_request, '管理-获取成员列表')
        payload = {
            "id": extracted_parameters,
            "password": md5.hexdigest()
        }
        print(payload)
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name, variables=payload)
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
    def delete_user(cls, http_request, test_case_name):
        """
        删除用户
        :param http_request:
        :param test_case_name:
        :return:
        """
        response, extracted_parameters, assert_code, case_id = cls.get_user_id(http_request, '管理-获取成员列表')

        payload = {
            'id':extracted_parameters
        }
        print(
            payload
        )
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name, variables=payload)
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