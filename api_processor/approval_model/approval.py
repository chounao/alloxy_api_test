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

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            jsonpath_expr="$.data.list[0].id",
            error_msg="获取审批数据失败")



    @classmethod
    def get_approval_data_for_approved(cls,http_request,test_case_name):
        """
        获取审批数据
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 审批数据
        """

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            jsonpath_expr="$.data",
            error_msg="获取审批数据失败"
        )

    @classmethod
    def get_approval_detail(cls,http_request,approval_status):
        """
        :param http_request:
        :return:
        """
        response, extracted_parameters, assert_code, case_id = http_request.execute_case(http_request,test_case_name = '获取审批列表')

        prams = {
            "approval_log_id": extracted_parameters,
            "status": approval_status
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
        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables=prams,
            error_msg="操作审核失败")

