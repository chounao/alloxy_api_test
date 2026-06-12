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
        """
        获取审批设置
        :param http_request:
        :param test_case_name:
        :return:
        """
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            error_msg="获取审批设置失败")


    @classmethod
    def create_trx_review_settings(cls,http_request,test_case_name):
        """
        创建审批设置
        :param http_request:
        :param test_case_name:
        :return:
        """
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
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables=payload,
            error_msg="创建审批设置失败")

    @classmethod
    def find_create_trx_review_settings_data(cls,http_request,name):
        """
        查找创建审批设置数据
        :param http_request:
        :param name:
        :return:
        """

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name='管理-获取审批设置列表',
            jsonpath_expr=f'$.data.list[?(@.name == "{name}")].id',
            error_msg="查找创建审批设置数据失败")

    @classmethod
    def update_trx_review_settings(cls,http_request,test_case_name):
        """
        更新审批设置
        :param http_request:
        :param test_case_name:
        :return:
        """
        response, extracted_parameters, assert_code, case_id = cls.find_create_trx_review_settings_data(http_request,cls.risk_settings_name)
        payload = {
            "id": extracted_parameters,
            "name": cls.up_risk_settings_name
        }
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables=payload,
            error_msg="更新审批设置失败")


    @classmethod
    def delete_trx_review_settings(cls,http_request,test_case_name):
        """
        删除审批设置
        :param http_request:
        :param test_case_name:
        :return:
        """
        extracted_parameters = cls.find_create_trx_review_settings_data(http_request,cls.up_risk_settings_name)
        payload = {
            "id": extracted_parameters
        }
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables=payload,
            error_msg="删除审批设置失败")





    """
    风控策略设置
    """
    @classmethod
    def get_risk_policy_settings(cls,http_request,test_case_name):
        """
        获取风控策略设置
        :param http_request:
        :param test_case_name:
        :return:
        """
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            error_msg="获取风控策略设置失败")

    @classmethod
    def find_create_risk_policy_settings_data(cls,http_request):
        """
        查找或创建风控策略设置数据
        :param http_request:
        :return:
        """

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name='管理-查询风控设置',
            jsonpath_expr=f'$.data[*].id',
            error_msg="查找创建风控策略设置数据失败")



    @classmethod
    def create_risk_policy_settings(cls,http_request,test_case_name):
        """
        创建风控策略设置
        :param http_request:
        :param test_case_name:
        :return:
        """
        payload = {
            "name": cls.risk_settings_name,
        }

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables= payload,
            error_msg="创建风控策略设置失败")

    @classmethod
    def delete_risk_policy_settings(cls,http_request,test_case_name):
        """
        删除风控策略设置
        :param http_request:
        :param test_case_name:
        :return:
        """
        payload = {
            "id": cls.get_risk_policy_settings(http_request,'管理-获取风控策略列表')[1],
        }

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables=payload,
            error_msg="删除风控策略设置失败")


    """
    
    白名单
    """
    @classmethod
    def get_trx_namelist_white_list(cls,http_request,test_case_name):
        """
        获取白名单
        :param http_request:
        :param test_case_name:
        :return:
        """
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            error_msg="获取白名单失败")
    @classmethod
    def find_get_trx_namelist_white_list_data(cls, http_request):
        """
        查找或获取白名单数据
        :param http_request:
        :return:
        """
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

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name='管理-查询白名单列表',
            jsonpath_expr=f'$.data.list[*].id',
            error_msg="获取白名单失败")
    @classmethod
    def create_trx_namelist_white_list(cls,http_request,test_case_name,payload):
        """
        创建白名单
        :param http_request:
        :param test_case_name:
        :param payload:
        :return:
        """

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables=payload,
            error_msg="创建白名单失败")
    @classmethod
    def delete_trx_namelist_white_list(cls,http_request,test_case_name):
        """
        删除白名单
        :param http_request:
        :param test_case_name:
        :return:
        """
        id = cls.find_get_trx_namelist_white_list_data(http_request)
        if type(id) == list:
            data = random.choice(id)
        else:
            data = id

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            replace_data={"id": data},
            error_msg="删除白名单失败")
    @classmethod
    def get_trx_namelist_write_log(cls,http_request,test_case_name):
        """
        获取白名单写入日志
        :param http_request:
        :param test_case_name:
        :return:
        """
        id = cls.find_get_trx_namelist_white_list_data(http_request)
        if type(id) == list:
            data = random.choice(id)
        else:
            data = id

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            replace_data={"id": data},
            error_msg="获取白名单写入日志失败")
    """
    
    黑名单流程
    """
    @classmethod
    def get_trx_namelist_black_list(cls,http_request,test_case_name):
        """
        获取黑名单
        :param http_request:
        :param test_case_name:
        :return:
        """

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            error_msg="获取黑名单失败")
    @classmethod
    def find_get_trx_namelist_black_list_data(cls,http_request):
        """
        查找或获取黑名单数据
        :param http_request:
        :return:
        """

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name = '管理-查询黑名单列表',
            jsonpath_expr=f'$.data.list[*].id',
            error_msg="查找获取黑名单数据失败")

    @classmethod
    def create_trx_namelist_black_list(cls,http_request,test_case_name,payload):
        """
        创建黑名单
        :param http_request:
        :param test_case_name:
        :param payload:
        :return:
        """
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables=payload,
            error_msg="创建黑名单失败")
    @classmethod
    def get_trx_namelist_black_log(cls,http_request,test_case_name):
        """
        获取黑名单写入日志
        :param http_request:
        :param test_case_name:
        :return:
        """
        id = cls.find_get_trx_namelist_black_list_data(http_request)
        if type(id) == list:
            data = random.choice(id)
        else:
            data = id

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            replace_data={"id": data},
            error_msg="获取黑名单写入日志失败")



    @classmethod
    def delete_trx_namelist_black_list(cls,http_request,test_case_name):
        """
        删除黑名单
        :param http_request:
        :param test_case_name:
        :return:
        """
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
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            replace_data={"id": data}    ,
            error_msg="删除黑名单失败")




