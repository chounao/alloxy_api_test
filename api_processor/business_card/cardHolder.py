from math import radians
from random import random

import Common.logger as logger


logger = logger.logger



class CardHolderManagement:
    sheet_name = 'Card_page'

    #查询持卡人之前需要查询部门接口

    @classmethod
    def get_department_id(cls, http_request, test_case_name):
        """
        获取部门ID
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 部门ID
        """

        try :
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                nested_keys=['data']
            )
            if result is None or len(result) != 4:
                logger.error("返回结果格式不正确")
                return None, None, None, None
            response, extracted_parameters, assert_code, case_id = result
            if response is not None:
                return response, extracted_parameters, assert_code, case_id
            else:
                logger.error("请求失败，无响应返回")
                return response, None, assert_code, case_id
        except Exception as e:
            logger.error(f"获取钱包交易详情失败: {e}")

    @classmethod
    def get_department_id_data(cls, http_request):
        """
        获取部门ID
        :param http_request: HttpRequest实例
        :return: 部门ID
        """
        result = cls.get_department_id(http_request, '管理-获取部门列表')
        if result is None:
            return None
        else:
            response, extracted_parameters, assert_code, case_id = result
            if response is None:
                logger.error("请求失败，无响应返回")
                return None
            else:
                department_id = extracted_parameters[0].get('department_id', None)
                logger.info(f"部门ID为：{department_id}")
                return department_id
    #持卡人查询接口
    @classmethod
    def get_card_holder_info(cls, http_request, test_case_name, body=None, page=1, take=20, max_pages=None):
        """
        获取持卡人信息
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :param body: 请求体参数（可选）
        :param page: 起始页码，默认为1
        :param take: 每页数据条数，默认为100
        :param max_pages: 最大查询页数，None表示查询所有页面
        :return: 合并后的所有页面数据
        """
        all_extracted_parameters = []
        current_page = page

        while True:
            data = {
                'page': current_page,
                'take': take,
            }

            # 明确判断 body 是否有效再合并
            if isinstance(body, dict):
                data.update(body)

            try:
                result = http_request._send_request(
                    cls.sheet_name,
                    test_case_name,
                    dict_data=data,
                    nested_keys=['data', 'list']
                )

                # 统一返回格式，始终返回四元素元组
                if result is None or not isinstance(result, (list, tuple)) or len(result) != 4:
                    logger.error(f"[{test_case_name}] 返回结果格式不正确: {result}")
                    break

                response, extracted_parameters, assert_code, case_id = result

                if response is None:
                    logger.error(f"[{test_case_name}] 请求失败，无响应返回")
                    break

                # 检查是否有数据返回
                if not extracted_parameters:
                    logger.info(f"[{test_case_name}] 第{current_page}页无数据，停止查询")
                    break

                # 合并当前页数据
                all_extracted_parameters.extend(extracted_parameters)

                # 检查是否还有下一页
                total_count = response.get('data', {}).get('count', 0)
                current_total = current_page * take

                # 如果已经达到最大页数限制或没有更多数据，则停止
                if (max_pages and current_page >= max_pages) or current_total >= total_count:
                    logger.info(f"[{test_case_name}] 已达到最大页数限制或无更多数据")
                    break

                current_page += 1

            except Exception as e:
                logger.error(f"[{test_case_name}] 获取钱包交易数据失败: {e}")
                break

        # 返回合并后的所有数据
        return response, extracted_parameters, assert_code, case_id

    def get_card_holder_info_data(cls, http_request, body=None):
        """
        获取持卡人信息
        :param http_request: HttpRequest实例
        :param body: 请求体参数（可选）
        :param kyc_review_status: KYC审核状态（可选）
        :return: 持卡人ID列表
        """
        id_list = []
        try:
            result = cls.get_card_holder_info(http_request, '获取虚拟卡持有人列表', body)

            if result is None:
                return []

            response, extracted_parameters, assert_code, case_id = result
            print(extracted_parameters)
            if response is None:
                logger.error("请求失败，无响应返回")
                return []
            else:
                for i in extracted_parameters:

                    id_list.append(i.get('id'))

            logger.info(f"获取到持卡人ID列表为：{id_list}")
            return id_list

        except Exception as e:
            logger.error(f"获取持卡人列表数据时发生异常: {str(e)}")
            return []


    #操作持卡人
    @classmethod
    def operate_card_holder(cls, http_request, test_case_name, body= None):
        """
        操作持卡人  取持卡人详情 ，所有状态都可以
                    删除持卡人 ：只有未通过已过期可以删除
                    冻结/解冻持卡人 ：只有完成状态
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :param find_card_holder_dict: 筛选条件字典
        :return: 操作结果
        """


        card_holder_data = cls.get_card_holder_info_data(http_request, body)
        if not card_holder_data:
            raise ValueError("持卡人信息数据为空")
        # 从持卡人数据中随机选择一个持卡人ID
        card_holder_id = random.choice(card_holder_data)

        try:
            if len(card_holder_id) == 0:
                logger.error(f"[{test_case_name}] 未找到符合条件的持卡人ID")
                return None
            else:
                result = http_request._send_request(
                    cls.sheet_name,
                    test_case_name,
                    replace_data={'id': card_holder_id},
                )

                if result is None or not isinstance(result, (list, tuple)) or len(result) != 4:
                    logger.error(f"[{test_case_name}] 返回结果格式不正确: {result}")
                    return None

                response, extracted_parameters, assert_code, case_id = result

                if response is None:
                    logger.error(f"[{test_case_name}] 请求失败，无响应返回")
                    return None

                return response

        except Exception as e:
            logger.error(f"[{test_case_name}] 获取持卡人详情失败: {e}")

    #冻结
    @classmethod
    def freeze_or_thawing_card_holder(cls, http_request, test_case_name,status, body=None):
        """
        冻结持卡人 只有完成状态
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :param card_holder_id: 持卡人ID
        :param status: 状态
        :return: 冻结结果数据
        """
        data = {
            'status':status
        }
        card_holder_data = cls.get_card_holder_info_data(http_request, body)
        if not card_holder_data:
            raise ValueError("持卡人信息数据为空")
        card_holder_id = card_holder_data[0]
        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                dict_data={'id': card_holder_id},
                variables=data
            )

            if result is None or not isinstance(result, (list, tuple)) or len(result) != 4:
                logger.error(f"[{test_case_name}] 返回结果格式不正确: {result}")
                return None

            response, extracted_parameters, assert_code, case_id = result

            if response is None:
                logger.error(f"[{test_case_name}] 请求失败，无响应返回")
                return None

            return response

        except Exception as e:
            logger.error(f"[{test_case_name}] 冻结持卡人失败: {e}")
    #根据部门id获取对应的的人员
    @classmethod
    def get_card_holder_by_department_id(cls, http_request, test_case_name):
        """
        根据部门ID获取对应的人员
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :return: 人员列表
        """
        id = cls.get_department_id_data(http_request)
        if not id:
            raise ValueError("部门ID数据为空")
        else:
            department_id = f'department_id = {id}'
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                ping_data=department_id
            )
            if result is None or not isinstance(result, (list, tuple)) or len(result) != 4:
                logger.error(f"[{test_case_name}] 返回结果格式不正确: {result}")
                return None

            response, extracted_parameters, assert_code, case_id = result

            if response is None:
                logger.error(f"[{test_case_name}] 请求失败，无响应返回")
                return None

            return response



    #创建持卡人参数
    @classmethod
    def create_card_holder_params(cls,department, user,country):
        """
        创建制卡人参数
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :param body: 请求体参数（可选）
        :return: 制卡人参数
        """
        # 增加基本的空值检查，防止因前置数据获取失败导致的崩溃
        if not user or not country or department is None:
            raise ValueError("创建持卡人参数失败：部门、用户或国家信息不能为空")

        try:
            user_id = user['id']
            first_name = user['first_name']
            last_name = user['last_name']
            phone = user.get('phone', '13800138000')  # 提供默认值防止 KeyError
            email = user.get('email', 'test@example.com')

            country_name = country['country_name']
            # 安全获取省份，防止 province 列表为空
            province_list = country.get('province', [])
            province = province_list[0]['province_name'] if province_list else "DefaultProvince"
            iso_code = country.get('iso3', 'CHN')  # 修正变量名 ios_code -> iso_code

            params = {
                "is_external": 0,
                "first_name": first_name,
                "last_name": last_name,
                "id_document_type": "Passport",
                "id_document_number": "E12345678",  # 建议使用更规范的格式
                "birthday": "2000-01-01",
                "phone": phone,
                "email": email,
                "label": "test_auto",
                "country": country_name,
                "province": province,
                "city": "TestCity",
                "address": "123 Test Street",
                "rbac_department_id": department,
                "user_id": user_id,
                "area_code": "86",
                "iso_code": iso_code
            }
            return params
        except KeyError as e:
            raise KeyError(f"用户或国家数据结构异常，缺少必要字段: {e}")
    #新建制卡人
    @classmethod
    def create_card_holder(cls, http_request, test_case_name, department, user,country):
        """
        新建制卡人
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :param body: 请求体参数（可选）
        """
        body = cls.create_card_holder_params(department, user,country)

        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                variables= body,
                jsonpath_expr="$.data.virtualCardHolderKyc.kyc_er_id"
            )
            if result is None or not isinstance(result, (list, tuple)) or len(result) != 4:
                logger.error(f"[{test_case_name}] 返回结果格式不正确: {result}")
                return None

            response, extracted_parameters, assert_code, case_id = result

            if response is None:
                logger.error(f"[{test_case_name}] 请求失败，无响应返回")
                return None
            if response is not None:
                logger.info(f'id:{extracted_parameters}')
            return response

        except Exception as e:
            logger.error(f"[{test_case_name}] 创建卡人失败: {e}")


