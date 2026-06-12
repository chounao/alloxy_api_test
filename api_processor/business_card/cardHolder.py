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


        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            nested_keys=['data'],
            error_msg="获取部门列表失败"
             )
    @classmethod
    def get_department_id_data(cls, http_request):
        """
        获取部门ID
        :param http_request: HttpRequest实例
        :return: 部门ID
        """
        response, extracted_parameters, assert_code, case_id = cls.get_department_id(http_request, '管理-获取部门列表')

        if response is None:
            logger.error("请求失败，无响应返回")
            return None
        else:
            department_id = extracted_parameters[0].get('department_id', None)
            logger.info(f"部门ID为：{department_id}")
            return department_id
    #持卡人查询接口
    @classmethod
    def get_card_holder_info(cls, http_request, test_case_name, extra_params=None, page=1, take=100, max_pages=None):
        """
        获取持卡人信息（支持分页查询并合并所有数据）
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :param extra_params: 额外请求参数（可选）
        :param page: 起始页码，默认为1
        :param take: 每页数据条数，默认为100
        :param max_pages: 最大查询页数，None表示查询所有页面
        :return: tuple(response, all_data, assert_code, case_id)
        """
        all_data = []
        current_page = page
        last_response = None
        last_assert_code = None
        last_case_id = None

        logger.info(f"[{test_case_name}] 开始分页查询，起始页:{page}, 每页:{take}, 最大页数:{max_pages}")

        while True:
            # 构建请求参数
            data = {'page': current_page, 'take': take}
            if isinstance(extra_params, dict):
                data.update(extra_params)

            try:
                response, extracted_data, assert_code, case_id = http_request.execute_case(
                    sheet_name=cls.sheet_name,
                    test_case_name=test_case_name,
                    dict_data=data,
                    nested_keys=['data', 'list'],
                    error_msg="获取持卡人列表失败"
                )

                # 保存最后一次的响应信息
                last_response = response
                last_assert_code = assert_code
                last_case_id = case_id

                if response is None:
                    logger.error(f"[{test_case_name}] 第{current_page}页请求失败，无响应返回")
                    break

                # 检查是否有数据返回
                if not extracted_data:
                    logger.info(f"[{test_case_name}] 第{current_page}页无数据，停止查询")
                    break

                # 合并当前页数据
                all_data.extend(extracted_data)
                logger.debug(
                    f"[{test_case_name}] 第{current_page}页获取到{len(extracted_data)}条数据，累计{len(all_data)}条")

                # 检查是否还有下一页
                total_count = response.get('data', {}).get('count', 0)
                current_total = current_page * take

                # 判断是否停止查询
                should_stop = False
                if max_pages and current_page >= max_pages:
                    logger.info(f"[{test_case_name}] 已达到最大页数限制({max_pages}页)，停止查询")
                    should_stop = True
                elif current_total >= total_count:
                    logger.info(f"[{test_case_name}] 已获取全部数据({total_count}条)，停止查询")
                    should_stop = True

                if should_stop:
                    break

                current_page += 1

            except Exception as e:
                logger.error(f"[{test_case_name}] 第{current_page}页查询失败: {e}")
                break

        logger.info(f"[{test_case_name}] 分页查询完成，共获取{len(all_data)}条数据")
        return last_response, all_data, last_assert_code, last_case_id

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


        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            replace_data={'id': card_holder_id},
            error_msg="操作持卡人失败"
        )

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
        return http_request.execute_case(
                sheet_name=cls.sheet_name,
                test_case_name=test_case_name,
                dict_data={'id': card_holder_id},
                variables=data,
                error_msg="冻结持卡人失败"
            )
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
            return http_request.execute_case(
                    sheet_name=cls.sheet_name,
                    test_case_name=test_case_name,
                    ping_data=department_id,
                    error_msg="根据部门ID获取持卡人失败"
            )




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

        return http_request.execute_case(
            sheet_name=cls.sheet_name,
            test_case_name=test_case_name,
            variables=body,
            jsonpath_expr="$.data.virtualCardHolderKyc.kyc_er_id",
            error_msg="创建制卡人失败"
        )


