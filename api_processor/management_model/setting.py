import Common.logger as logger
logger = logger.logger
from Common.read_and_save_tool import ConfigTools
import random
class Settings:
    sheet_name = 'management_page'
    risk_settings_name = "复核规则001"
    up_risk_settings_name = "复核规则002"

    """
    
    审批设置
    """
    @classmethod
    def get_trx_review_settings(cls,http_request,test_case_name):
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name)
            if result is None or len(result) != 4:
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("获取数据，无响应返回")
        except Exception as e:
            logger.error(f"失败: {e}")
            raise e


    @classmethod
    def create_trx_review_settings(cls,http_request,test_case_name):
        payload = {
            "name": cls.risk_settings_name,
        }
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name,variables= payload)
            if result is None or len(result) != 4:
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("获取数据，无响应返回")
        except Exception as e:
            logger.error(f"失败: {e}")
            raise e

    @classmethod
    def find_create_trx_review_settings_data(cls,http_request,name):
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name = '管理-获取审批设置列表',jsonpath_expr=f'$.data.list[?(@.name == "{name}")].id')
            if result is None or len(result) != 4:
                return None, None, None, None
            response, extracted_parameters, assert_code, case_id = result
            print(extracted_parameters)
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return extracted_parameters
            else:
                logger.error("获取数据，无响应返回")
        except Exception as e:
            logger.error(f"失败: {e}")
            raise e

    @classmethod
    def update_trx_review_settings(cls,http_request,test_case_name):
        extracted_parameters, = cls.find_create_trx_review_settings_data(http_request,cls.risk_settings_name)
        payload = {
            "id": extracted_parameters,
            "name": cls.up_risk_settings_name
        }
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name,variables= payload)
            if result is None or len(result) != 4:
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("获取数据，无响应返回")
        except Exception as e:
            logger.error(f"失败: {e}")
            raise e



    @classmethod
    def delete_trx_review_settings(cls,http_request,test_case_name):
        extracted_parameters = cls.find_create_trx_review_settings_data(http_request,cls.up_risk_settings_name)
        payload = {
            "id": extracted_parameters
        }
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name,variables= payload)
            if result is None or len(result) != 4:
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error(
                    "获取数据，无响应返回"
                )
        except Exception as e:
            logger.error(f"失败: {e}")
            raise e






    """
    风控策略设置
    """
    @classmethod
    def get_risk_policy_settings(cls,http_request,test_case_name):
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name)
            if result is None or len(result) != 4:
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("获取数据，无响应返回")
        except Exception as e:
            logger.error(f"失败: {e}")
            raise e


    @classmethod
    def find_create_risk_policy_settings_data(cls,http_request):
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name = '管理-查询风控设置',jsonpath_expr=f'$.data[*].id')
            if result is None or len(result) != 4:
                return None, None, None, None
            response, extracted_parameters, assert_code, case_id = result
            print(extracted_parameters)
            if response is not None:
                logger.info(f'id:{extracted_parameters}')

                return extracted_parameters
            else:
                logger.error("获取数据，无响应返回")
        except Exception as e:
            logger.error(f"失败: {e}")
            raise e



    @classmethod
    def create_risk_policy_settings(cls,http_request,test_case_name):
        payload = {
            "name": cls.risk_settings_name,
        }
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name,variables= payload)
            if result is None or len(result) != 4:
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("获取数据，无响应返回")
        except Exception as e:
            logger.error(f"失败: {e}")
            raise e

    @classmethod
    def delete_risk_policy_settings(cls,http_request,test_case_name):
        payload = {
            "id": cls.get_risk_policy_settings(http_request,'管理-获取风控策略列表')[1],
        }
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name,variables= payload)
            if result is None or len(result) != 4:
                return None, None, None, None
            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error(
                    "获取数据，无响应返回"
                )
                return None, None, None, None
        except Exception as e:
            logger.error(f"失败: {e}")
            raise e




    """
    
    白名单
    """
    @classmethod
    def get_trx_namelist_white_list(cls,http_request,test_case_name):
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name)
            if result is None or len(result) != 4:
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("获取数据，无响应返回")
        except Exception as e:
            logger.error(f"失败: {e}")
            raise e

    @classmethod
    def find_get_trx_namelist_white_list_data(cls, http_request):
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name='管理-查询白名单列表',
                                                jsonpath_expr=f'$.data.list[*].id')
            if result is None or len(result) != 4:
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                print(extracted_parameters)
                return extracted_parameters
            else:
                logger.error("获取数据，无响应返回")
                return None, None, None, None
        except Exception as e:
            logger.error(f"失败: {e}")
    @classmethod
    def create_trx_namelist_white_list(cls,http_request,test_case_name,payload):

        try:
            result = http_request._send_request(cls.sheet_name, test_case_name, variables=payload)
            if result is None or len(result) != 4:
                return None, None, None
            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error(
                    "获取数据，无响应返回"
                )
        except Exception as e:
            logger.error(f"失败: {e}")

    @classmethod
    def delete_trx_namelist_white_list(cls,http_request,test_case_name):
        id = cls.find_get_trx_namelist_white_list_data(http_request)
        if type(id) == list:
            data = random.choice(id)
        else:
            data = id
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name,replace_data={"id": data})
            if result is None or len(result) != 4:
                return None, None, None, None
            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error(
                    "获取数据，无响应返回"
                )
        except Exception as e:
            logger.error(f"失败: {e}")
            raise e

    @classmethod
    def get_trx_namelist_write_log(cls,http_request,test_case_name):
        id = cls.find_get_trx_namelist_white_list_data(http_request)
        if type(id) == list:
            data = random.choice(id)
        else:
            data = id
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name,replace_data={"id": data})
            if result is None or len(result) != 4:
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("获取数据，无响应返回")
                return None, None, None, None
        except Exception as e:
            logger.error(f"失败: {e}")
            raise e


    """
    
    黑名单流程
    """
    @classmethod
    def get_trx_namelist_black_list(cls,http_request,test_case_name):
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name)
            if result is None or len(result) != 4:
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("获取数据，无响应返回")
                return None, None, None, None
        except Exception as e:
            logger.error(f"失败: {e}")
    @classmethod
    def find_get_trx_namelist_black_list_data(cls,http_request):
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name = '管理-查询黑名单列表',jsonpath_expr=f'$.data.list[*].id')
            if result is None or len(result) != 4:
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                print(extracted_parameters)
                return  extracted_parameters
            else:
                logger.error("获取数据，无响应返回")
                return None, None, None, None
        except Exception as e:
            logger.error(f"失败: {e}")

    @classmethod
    def create_trx_namelist_black_list(cls,http_request,test_case_name,payload):
        # payload = {
        #     "name": cls.trx_namelist_black_list_name,
        # }
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name,variables= payload)
            if result is None or len(result) != 4:
                return None, None, None
            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error(
                    "获取数据，无响应返回"
                )
        except Exception as e:
            logger.error(f"失败: {e}")
    @classmethod
    def get_trx_namelist_black_log(cls,http_request,test_case_name):
        id = cls.find_get_trx_namelist_black_list_data(http_request)
        if type(id) == list:
            data = random.choice(id)
        else:
            data = id
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name,replace_data={"id": data})
            if result is None or len(result) != 4:
                return None, None, None, None

            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(
                    f'id:{extracted_parameters}'
                )
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error(
                    "获取数据，无响应返回"
                )
        except Exception as e:
            logger.error(f"失败: {e}")




    @classmethod
    def delete_trx_namelist_black_list(cls,http_request,test_case_name):
        id = cls.find_get_trx_namelist_black_list_data(http_request)
        if type(id) == list:
            data = random.choice(id)
        else:
            data = id
        try:
            result = http_request._send_request(cls.sheet_name, test_case_name,replace_data={"id": data})
            if result is None or len(result) != 4:
                return None, None, None, None
            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error(
                    "获取数据，无响应返回"
                )
        except Exception as e:
            logger.error(f"失败: {e}")




