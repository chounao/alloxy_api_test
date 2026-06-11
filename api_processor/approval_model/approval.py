import Common.logger as logger
logger = logger.logger

class Approval:
    sheet_name = 'Approval'


    @classmethod
    def get_approval_data_for_pending(cls,http_request,test_case_name):
        """
        获取审批数据
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 审批数据
        """
        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                jsonpath_expr="$.data.list[0].id",
            )
            if result is None or len(result) != 4:
                logger.error("返回结果格式不正确")
                return None, None, None, None
            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'获取的审批数据为:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("请求失败，无响应返回")
                return response, None, assert_code, case_id
        except Exception as e:
            logger.error(f"详情失败: {e}")






    @classmethod
    def get_approval_data_for_approved(cls,http_request,test_case_name):
        """
        获取审批数据
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 审批数据
        """
        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                jsonpath_expr="$.data",
            )
            if result is None or len(result) != 4:
                logger.error("返回结果格式不正确")
                return None, None, None, None
            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'获取的审批数据为:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("请求失败，无响应返回")
                return response, None, assert_code, case_id
        except Exception as e:
            logger.error(f"详情失败: {e}")

    @classmethod
    def get_approval_detail(cls,http_request,approval_status):
        """
        :param http_request:
        :return:
        """
        result = cls.get_approval_data_for_pending(http_request,test_case_name = '获取审批列表')
        response, extracted_parameters, assert_code, case_id = result
        prams = {
            "approval_log_id":extracted_parameters,
            "status":approval_status
        }
        return prams

    #操作审核
    @classmethod
    def operation_approval(cls,http_request,test_case_name,approval_status):
        """
        操作审核
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :param approval_id: 审批id
        :param approval_status: 审批状态
        :return: 审批结果
        """
        prams = cls.get_approval_detail(http_request,approval_status)
        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                variables=prams

            )
            if result is None or len(result) != 4:
                logger.error("返回结果格式不正确")
                return None, None, None, None
            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                logger.info(f'操作审核结果为:{extracted_parameters}')
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("请求失败，无响应返回")
                return response, None, assert_code, case_id
        except Exception as e:
            logger.error(f"详情失败: {e}")
