import random
from Common.simple_request import HttpRequest
import Common.logger as logger
logger = logger.logger



class HomePage:
    sheet_name = 'Home_page'




    @classmethod
    def get_user_data(cls,test_case_name,http_request):
        """
        获取登录数据
        """

        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
            )
            if result is None or len(result) != 4:
                logger.error("获取用户数据请求返回结果格式不正确")
                return None, None, None, None

            response, extracted_parameters, assert_code,case_id = result
            if response is not None:
                return response, extracted_parameters, assert_code,case_id
            else:
                logger.error("获取用户数据请求失败，无响应返回")
                return None, None, None, None


        except Exception as e:
            logger.error(f"获取用户数据失败: {e}")
            return None, None, None, None


    @classmethod
    def get_user_menus(cls,test_case_name,http_request):
        """
        获取用户菜单权限
        """
        try:


            result =http_request._send_request(
                cls.sheet_name,
                test_case_name,
            )
            if result is None or len(result) != 4:
                logger.error("获取用户菜单权限请求返回结果格式不正确")
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                return response, None, assert_code, case_id
            else:
                logger.error("获取用户菜单权限请求失败，无响应返回")
                return None, None, None, None
        except Exception as e:
            logger.error(f"获取用户菜单权限失败: {e}")
            raise e


    @classmethod
    def get_user_account_overview(cls,test_case_name,http_request,dict_key = None,list_key = None,list_value = None):
        """
        获取用户账户概览
        """
        transaction_id_list = []
        try:


            result =http_request._send_request(
                cls.sheet_name,
                test_case_name,
                nested_keys =['data',dict_key]
            )
            # print(result)
            if result is None or len(result) != 4:
                logger.error("获取用户相关数据请求返回结果格式不正确")
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                if extracted_parameters:
                    account_overview = extracted_parameters
                    if dict_key == 'balance_list':
                        for i in account_overview:
                            if i[list_key] == list_value:
                                return response, i, assert_code, case_id
                    if dict_key == 'transaction_list':
                        for i in account_overview:
                            if i['status'] == 'pending':
                                transacrion_id = i[list_key]
                                transaction_id_list.append(transacrion_id)
                        print(response, transaction_id_list, assert_code, case_id)
                        return response, transaction_id_list, assert_code, case_id

        except Exception as e:
            logger.error(f"获取用户角色权限失败: {e}")
            raise e

    @classmethod
    def get_todo_data(cls,test_case_name,http_request):
        """
        获取用户交易详情
        """
        try:


            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                nested_keys =['data']
            )
            print( result)
            if result is None or len(result) != 4:
                logger.error("获取用户菜单权限请求返回结果格式不正确")
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                if len(extracted_parameters['list']) != 0:
                    return response, extracted_parameters, assert_code, case_id
                else:
                    logger.error("获取用户交易详情请求无数据")
                    return response, None, assert_code, case_id
            else:
                logger.error("获取用户交易详情请求失败，无响应返回")
                return None, None, None, None

        except Exception as e:
            logger.error(f"获取待办失败: {e}")
            raise e


    @classmethod
    def get_notices(cls,test_case_name,http_request):
        """
        获取用户通知
        """
        try:


            result =  http_request._send_request(
                cls.sheet_name,
                test_case_name,
                nested_keys =['data']
            )
            print(result)
            if result is None or len(result) != 4:
                logger.error("获取用户通知请求返回结果格式不正确")
                return None, None, None, None
            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                if len(extracted_parameters['list']) != 0:
                    return response, extracted_parameters, assert_code, case_id
                else:
                    logger.error("获取用户通知请求无数据")
                    return response, None, assert_code, case_id
            else:
                logger.error("获取用户通知请求失败，无响应返回")
                return None, None, None, None
        except Exception as e:
            logger.error(f"获取用户通知失败: {e}")
            raise e

    @classmethod
    def get_transacton_detail(cls,test_case_name,http_request,transaction_id):
        """
        获取用户交易详情
        """
        try:


            result =  http_request._send_request(
                cls.sheet_name,
                test_case_name,
                replace_data = transaction_id
            )
            if result is None or len(result) != 4:
                logger.error("获取用户交易详情请求返回结果格式不正确")
                return None, None, None
            response, extracted_parameters, assert_code, case_id = result
            if response is not None:

                return response, None, assert_code, case_id
            else:
                logger.error("获取用户交易详情请求失败，无响应返回")
                return None, None, None, None

        except Exception as e:
            logger.error(f"获取用户交易详情失败: {e}")
            raise e

    @classmethod
    def _get_transaction_id(cls, http_request):
        """
        获取用户交易详情

        Args:
            test_case_name (str): 测试用例名称
            http_request (HttpRequest): HTTP请求实例

        Returns:
            str: 随机选择的交易ID，失败时返回None
        """
        try:
            result = cls.get_user_account_overview('账号信息统计', http_request, 'transaction_list', 'id')
            print( result)
            if result is None or len(result) != 4:
                logger.error("获取用户交易详情请求返回结果格式不正确")
                return None, None, None, None

            response, transaction_id_list, assert_code, case_id = result

            if transaction_id_list is None or len(transaction_id_list) == 0:
                logger.error("获取用户交易详情失败，无交易记录")
                return None

            return random.choice(transaction_id_list)

        except Exception as e:
            logger.error(f"获取交易ID失败: {e}")
            return None



if __name__ == '__main__':
    home = HomePage()
    http_request  = HttpRequest()
    home._get_transaction_id(http_request)
