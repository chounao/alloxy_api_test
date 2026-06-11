from Common.simple_request import HttpRequest
import hashlib
from Common.read_and_save_tool import ConfigTools
import Common.logger as logger
import traceback

logger = logger.logger


class Alloxy_login:
    @classmethod
    def get_login_data(cls):
        """
        获取登录数据

        Returns:
            tuple: (variables_pass, variables_lost_password, variables_lost_email)
                   包含正常、错误密码、错误邮箱的登录参数
        """
        config = ConfigTools()
        pass_word = config.get_login_data('PASSWORD')
        password = hashlib.md5(pass_word.encode('utf-8')).hexdigest()
        email = config.get_login_data('EMAIL')

        variables_pass = {
            'email': email,
            'password': password
        }
        variables_lost_password = {
            'email': email,
            'password': '0'
        }
        variables_lost_email = {
            'email': '0',
            'password': password
        }
        return variables_pass, variables_lost_password, variables_lost_email

    @classmethod
    def login(cls, test_case_name, variables):
        """
        执行用户登录操作

        Args:
            test_case_name (str): 测试用例名称
            variables (dict): 登录参数（email/password）
            http_request (HttpRequest): HTTP请求对象

        Returns:
            tuple: (access_token, status_code, assert_code, assert_amount, case_id)
                   登录成功时返回令牌和状态信息，失败时相应字段为None

        Raises:
            Exception: 登录过程中出现的异常
        """
        sheet_name = 'Login_page'
        logger.info(f"开始执行登录测试: {sheet_name}-{test_case_name}")
        http_request = HttpRequest()
        try:
            # 发送登录请求并获取访问令牌
            if hasattr(http_request, '_send_request'):
                result = http_request._send_request(
                    sheet_name,
                    test_case_name,
                    variables,
                    nested_keys=['data', 'accessToken']
                )

                # 验证返回结果格式
                if result is None or len(result) != 4:
                    logger.error(f"登录请求返回结果格式不正确: {result}")
                    return None, None, None, None

                response, extracted_parameters, assert_code, case_id = result

                # 处理登录响应
                if response is not None:
                    status_code = response.status_code
                    if extracted_parameters:
                        access_token = extracted_parameters
                        logger.info(f"登录成功，获取到的accessToken: {access_token}")
                        return access_token, status_code, assert_code, case_id
                    else:
                        logger.warning("登录失败，未获取到accessToken")
                        return None, status_code, assert_code, case_id
                else:
                    logger.error("登录请求失败，无响应返回")
                    return None, None, assert_code, case_id



        except Exception as e:
            logger.error(f"登录过程中出现异常: {e}")
            logger.error(traceback.format_exc())
            return None, None, None, None


if __name__ == '__main__':
    try:
        login = Alloxy_login()
        request_ = HttpRequest()
        variables_pass, variables_lost_password, variables_lost_email = login.get_login_data()

        # 测试正常登录
        result = login.login('登陆成功', variables=variables_pass)
        print(f"正常登录结果: {result}")

        # 测试异常登录
        result = login.login('登陆成功', variables=variables_lost_password)
        print(f"异常登录结果: {result}")

    except Exception as e:
        logger.error(f"测试执行失败: {e}")
