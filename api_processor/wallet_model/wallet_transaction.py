import Common.logger as logger
from api_processor.wallet_model.wallet_list_page import WalletListPage

logger = logger.logger


class WalletTransaction:
    sheet_name = 'Wallte_page'
    wallet_list_page = WalletListPage()


    @classmethod
    def get_transaction_data(cls, http_request, test_case_name, body=None, page=1, take=20, max_pages=None):
        """
        获取钱包交易数据（支持分页查询）
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
        return response, all_extracted_parameters, assert_code, case_id

    @classmethod
    def get_transaction_list_data(cls, http_request, body=None, find_transaction_dict: dict = None):
        """
        获取钱包交易列表
        :param http_request: HttpRequest实例
        :param body: 请求体参数
        :param find_transaction_dict: 查找交易的字典条件
        :return: 交易ID列表
        """
        id_list = []
        try:
            result = cls.get_transaction_data(http_request, '钱包-交易记录', body)
            if result is None:
                return []

            response, extracted_parameters, assert_code, case_id = result
            if response is None:
                logger.error("请求失败，无响应返回")
                return []

            for item in extracted_parameters:
                if find_transaction_dict is not None:
                    # 检查字典是否包含指定的键值对
                    match = True
                    for key, value in find_transaction_dict.items():
                        if key not in item or item[key] != value:
                            match = False
                            break
                    if match:
                        id_list.append(item['id'])
                else:
                    id_list.append(item['id'])

            logger.info(f"获取到的交易ID列表为：{id_list}")
            return id_list

        except Exception as e:
            logger.error(f"获取交易列表数据时发生异常: {str(e)}")
            return []

    #详情
    @classmethod
    def get_transaction_detail(cls, http_request, test_case_name, transaction_id):
        """
        获取钱包交易详情
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :param transaction_id: 交易ID
        :return:
        """
        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                replace_data={'id': transaction_id}
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

    #取消
    @classmethod
    def cancel_transaction(cls, http_request, test_case_name, transaction_id):
        """
        取消钱包交易
        :param http_request: HttpRequest实例
        :param test_case_name: 测试用例名称
        :param transaction_id: 交易ID
        :return:
        """
        data = {"id":transaction_id}
        try:
            result = http_request._send_request(
                cls.sheet_name,
                test_case_name,
                variables=data
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
            logger.error(f"取消钱包交易失败: {e}")
