from typing import Any, Callable, Iterable, Optional


class ApiProcessorError(RuntimeError):
    """业务处理层异常。"""


class BaseApiProcessor:
    """业务 API 处理器基类。

    中文备注：用于承接 wallet、management、business_card 等模块中的通用逻辑，
    比如执行用例、校验返回结构、从列表中查找目标记录、强制校验前置数据非空。
    """

    sheet_name: Optional[str] = None

    @classmethod
    def execute(
        cls,
        http_request,
        test_case_name: str,
        *,
        sheet_name: Optional[str] = None,
        variables: Optional[dict] = None,
        ping_data: Optional[str] = None,
        replace_data: Optional[dict] = None,
        dict_data: Optional[dict] = None,
        nested_keys: Optional[list] = None,
        jsonpath_expr: Optional[str] = None,
    ):
        target_sheet = sheet_name or cls.sheet_name
        if not target_sheet:
            raise ApiProcessorError(f"{cls.__name__} 未配置 sheet_name")
        return http_request.execute_case(
            sheet_name=target_sheet,
            test_case_name=test_case_name,
            variables=variables,
            ping_data=ping_data,
            replace_data=replace_data,
            dict_data=dict_data,
            nested_keys=nested_keys,
            jsonpath_expr=jsonpath_expr,
        )

    @staticmethod
    def unpack_result(result, case_name: str = ""):
        if result is None or not isinstance(result, (tuple, list)) or len(result) != 4:
            raise ApiProcessorError(f"{case_name} 返回结构异常，期望4元组，实际: {result}")
        return result

    @staticmethod
    def require_value(value: Any, message: str):
        if value in (None, "", [], {}):
            raise ApiProcessorError(message)
        return value

    @staticmethod
    def extract_list(payload: Any, *candidate_keys: str) -> list:
        """从常见响应结构中提取列表。

        中文备注：兼容 data、list、records、items 等常见字段，减少业务层重复判断。
        """
        if isinstance(payload, list):
            return payload
        if not isinstance(payload, dict):
            return []
        for key in candidate_keys or ("data", "list", "records", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
            if isinstance(value, dict):
                nested = BaseApiProcessor.extract_list(value)
                if nested:
                    return nested
        return []

    @staticmethod
    def find_first(records: Iterable[dict], predicate: Callable[[dict], bool]) -> Optional[dict]:
        for record in records or []:
            if isinstance(record, dict) and predicate(record):
                return record
        return None

    @classmethod
    def find_by_field(cls, records: Iterable[dict], field: str, expected: Any, *, required: bool = True):
        record = cls.find_first(records, lambda item: item.get(field) == expected)
        if required and record is None:
            raise ApiProcessorError(f"未找到目标记录: {field}={expected}")
        return record

    @classmethod
    def first_id_by_field(cls, records: Iterable[dict], field: str, expected: Any, id_field: str = "id"):
        record = cls.find_by_field(records, field, expected, required=True)
        return cls.require_value(record.get(id_field), f"目标记录缺少ID字段: {id_field}")
