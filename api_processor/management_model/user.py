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

        response, extracted_parameters, assert_code, case_id = http_request.execute_case(
            sheet_name=self.sheet_name,
            test_case_name='管理-获取部门列表',
            jsonpath_expr="$.data[0].children[?(@.name == 'test_001_name')].department_id",
            error_msg="获取部门列表失败"
        )
        department_id = extracted_parameters
        response, extracted_parameters, assert_code, case_id = http_request._send_request(
            self.sheet_name,
            test_case_name = '管理-获取角色列表',
            jsonpath_expr="$.data[?(@.name == 'test_001_name')].id",
            error_msg="获取角色列表失败"
        )


        role_id = extracted_parameters

        return department_id, role_id
    @classmethod
    def get_create_user_data(cls,http_request):
        """
        获取创建用户数据
        :param http_request: HttpRequest实例
        :return: 创建用户数据
        """
        department_id, role_id = cls.get_id_for_name(cls,http_request)
        fake = Faker('en_US')
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
        """
        创建用户
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 创建用户结果
        """
        payload  = cls.get_create_user_data(http_request)

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables= payload,
            error_msg="创建用户失败")

    @classmethod
    def get_user_id(cls,http_request,test_case_name):
        """
        获取用户id
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 用户id
        """

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            ping_data='page=1&take=10&name=',
            jsonpath_expr=f'$.data.data[?(@.first_name == \'{cls.create_first_name}\')].id',
            error_msg="获取用户id失败")
    @classmethod
    def update_user_info(cls, http_request,test_case_name):
        """
        更新用户信息
        :param http_request:
        :param test_case_name:
        :return:
        """
        payload  = cls.get_create_user_data(http_request)
        response, extracted_parameters, assert_code, case_id = cls.get_user_id(http_request, '管理-获取成员列表')
        payload['member_id'] = extracted_parameters
        payload['last_name'] = cls.PUT_last_name
        print( payload)

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables=payload,
            error_msg="更新用户信息失败")
    @classmethod
    def reset_password (cls, http_request, test_case_name):
        """
        重置密码
        :param http_request:
        :param test_case_name:
        :return:
        """
        md5 = hashlib.md5()
        md5.update(cls.pass_word.encode('utf-8'))
        response, extracted_parameters, assert_code, case_id = cls.get_user_id(http_request, '管理-获取成员列表')
        payload = {
            "id": extracted_parameters,
            "password": md5.hexdigest()
        }
        print(payload)

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables=payload,
            error_msg="重置密码失败")


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

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables=payload,
            error_msg="删除用户失败")