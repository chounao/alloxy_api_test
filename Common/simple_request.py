import json
import time
from typing import Any, Optional

import allure
import requests
from jsonpath_ng.ext import parse

from Common import excel_tools, logger, read_and_save_tool
from Common.execute import get_config_section


logger = logger.logger


class HttpRequest:
    """HTTP 请求客户端：负责用例读取、请求发送、响应提取和 Allure 附件。"""

    DEFAULT_TIMEOUT = 30
    SUPPORTED_METHODS = {"get", "post", "put", "delete", "patch"}

    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        self.config_section = get_config_section()
        self.logger = logger
        self.session = requests.Session()
        self.excel = excel_tools.ExcelTools()
        self.config = read_and_save_tool.ConfigTools()
        self.timeout = timeout
        self.headers = {
            "Content-Type": "application/json",
            "accept-language": "zh-cn",
            "accept": "application/json",
        }
        access_token = self.config.get_access_token()
        if access_token:
            self.headers["authorization"] = access_token
        self.session.headers.update(self.headers)

    def update_headers(self, headers: dict):
        if not isinstance(headers, dict):
            raise TypeError("headers必须是dict")
        self.headers.update(headers)
        self.session.headers.update(headers)
        return self.session

    def get_current_headers(self) -> dict:
        return dict(self.session.headers)

    def get_nested_value(self, data: Any, keys: list) -> Any:
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int) and 0 <= key < len(current):
                current = current[key]
            else:
                raise KeyError(f"嵌套路径不存在: {keys}; 断点: {key}")
        return current

    def extract_by_jsonpath(self, json_data: dict, jsonpath_expr: str):
        matches = [match.value for match in parse(jsonpath_expr).find(json_data)]
        if len(matches) == 1:
            return matches[0]
        return matches or None

    def _extract_response(self, response, nested_keys=None, jsonpath_expr=None):
        if not nested_keys and not jsonpath_expr:
            return None
        try:
            json_data = response.json()
        except ValueError as exc:
            raise AssertionError("响应体不是合法JSON，无法提取参数") from exc

        if jsonpath_expr:
            return self.extract_by_jsonpath(json_data, jsonpath_expr)
        return self.get_nested_value(json_data, nested_keys)

    def _attach_request(self, method: str, url: str, data: Optional[dict]) -> None:
        # 中文备注：敏感请求头脱敏后再写入 Allure，避免 token 泄露到报告。
        safe_headers = {
            key: ("***" if key.lower() in {"authorization", "cookie"} else value)
            for key, value in self.session.headers.items()
        }
        allure.attach(json.dumps({"method": method, "url": url, "headers": safe_headers}, ensure_ascii=False, indent=2),
                      name="请求信息", attachment_type=allure.attachment_type.JSON)
        if data is not None:
            allure.attach(json.dumps(data, ensure_ascii=False, indent=2), name="请求体",
                          attachment_type=allure.attachment_type.JSON)

    def _attach_response(self, response, elapsed_ms: int) -> None:
        content_type = response.headers.get("content-type", "")
        summary = {
            "status_code": response.status_code,
            "elapsed_ms": elapsed_ms,
            "headers": dict(response.headers),
        }
        allure.attach(json.dumps(summary, ensure_ascii=False, indent=2), name="响应摘要",
                      attachment_type=allure.attachment_type.JSON)
        attachment_type = allure.attachment_type.JSON if "json" in content_type else allure.attachment_type.TEXT
        allure.attach(response.text[:10000], name="响应体", attachment_type=attachment_type)

    def _dispatch(self, method: str, url: str, data: Optional[dict] = None):
        # 中文备注：所有 HTTP 方法统一从这里分发，减少 get/post/put/delete 重复逻辑。
        method = (method or "").lower()
        if method not in self.SUPPORTED_METHODS:
            raise ValueError(f"不支持的HTTP方法: {method}")

        request_kwargs = {"timeout": self.timeout}
        if method != "get" and data:
            request_kwargs["json"] = data

        self.logger.info("Making %s request to %s", method.upper(), url)
        started_at = time.perf_counter()
        response = self.session.request(method=method.upper(), url=url, **request_kwargs)
        elapsed_ms = int((time.perf_counter() - started_at) * 1000)
        self.logger.info("Response status code: %s, elapsed: %sms", response.status_code, elapsed_ms)
        self._attach_response(response, elapsed_ms)
        return response

    def request(
        self,
        api_name: str = None,
        ping_data: str = None,
        replace_data: dict = None,
        dict_data: dict = None,
        data: dict = None,
        nested_keys: Optional[list] = None,
        jsonpath_expr: Optional[str] = None,
    ):
        result = self.config.get_data_from_name(
            api_name=api_name, ping_data=ping_data, replace_data=replace_data, dict_data=dict_data
        )
        if result is None:
            raise ValueError(f"API配置不存在: {api_name}")
        method, url = result
        self._attach_request(method, url, data)
        response = self._dispatch(method, url, data)
        response.raise_for_status()
        return self._extract_response(response, nested_keys, jsonpath_expr) if (nested_keys or jsonpath_expr) else response

    def requests(self, method, url, data: dict = None, nested_keys: Optional[list] = None,
                 jsonpath_expr: Optional[str] = None):
        self._attach_request(method, url, data)
        response = self._dispatch(method, url, data)
        response.raise_for_status()
        return self._extract_response(response, nested_keys, jsonpath_expr) if (nested_keys or jsonpath_expr) else response

    def _request(
        self,
        sheet_name: str = None,
        test_case_name: str = None,
        variables: dict = None,
        ping_data: str = None,
        replace_data: dict = None,
        dict_data: dict = None,
        data: dict = None,
        nested_keys: Optional[list] = None,
        jsonpath_expr: Optional[str] = None,
    ):
        # 中文备注：从 Excel 读取 method/url/body/assert_code/case_id，并合并动态变量。
        method, url, excel_data, assert_code, case_id = self.excel.update_test_case_result(
            sheet_name=sheet_name,
            test_case_name=test_case_name,
            variables=variables,
            ping_data=ping_data,
            replace_data=replace_data,
            dict_data=dict_data,
        )
        request_data = data if data is not None else excel_data

        with allure.step(f"执行接口用例: {test_case_name}"):
            allure.dynamic.title(test_case_name)
            if case_id:
                allure.dynamic.id(str(case_id))
            allure.dynamic.label("sheet", sheet_name or "")
            allure.dynamic.label("method", method.upper())
            self._attach_request(method, url, request_data)
            try:
                response = self._dispatch(method, url, request_data)
                extracted = self._extract_response(response, nested_keys, jsonpath_expr)
                return response, extracted, assert_code, case_id
            except requests.RequestException as exc:
                self.logger.exception("[%s] HTTP请求异常", test_case_name)
                allure.attach(str(exc), name="请求异常", attachment_type=allure.attachment_type.TEXT)
                raise
            except Exception as exc:
                self.logger.exception("[%s] 执行异常", test_case_name)
                allure.attach(str(exc), name="执行异常", attachment_type=allure.attachment_type.TEXT)
                raise

    def execute_case(self, sheet_name: str = None, test_case_name: str = None, variables: dict = None,
                     ping_data: str = None, replace_data: dict = None, dict_data: dict = None,
                     data: dict = None, nested_keys: Optional[list] = None,
                     jsonpath_expr: Optional[str] = None):
        # 中文备注：对外主入口，返回结构固定为 response、提取参数、预期状态码、用例ID。
        return self._request(
            sheet_name=sheet_name,
            test_case_name=test_case_name,
            variables=variables,
            ping_data=ping_data,
            replace_data=replace_data,
            dict_data=dict_data,
            data=data,
            nested_keys=nested_keys,
            jsonpath_expr=jsonpath_expr,
        )

    _send_request = execute_case
    send_request = request
    send_requests = requests

    def get(self, url: str, nested_keys: Optional[list] = None, jsonpath_expr: Optional[str] = None):
        return self.requests("get", url, nested_keys=nested_keys, jsonpath_expr=jsonpath_expr)

    def post(self, url: str, data: dict = None, nested_keys: Optional[list] = None,
             jsonpath_expr: Optional[str] = None):
        return self.requests("post", url, data=data, nested_keys=nested_keys, jsonpath_expr=jsonpath_expr)

    def put(self, url: str, data: dict = None, nested_keys: Optional[list] = None, jsonpath_expr: Optional[str] = None):
        return self.requests("put", url, data=data, nested_keys=nested_keys, jsonpath_expr=jsonpath_expr)

    def delete(self, url: str, data: dict = None, nested_keys: Optional[list] = None,
               jsonpath_expr: Optional[str] = None):
        return self.requests("delete", url, data=data, nested_keys=nested_keys, jsonpath_expr=jsonpath_expr)

    def patch(self, url: str, data: dict = None, nested_keys: Optional[list] = None,
              jsonpath_expr: Optional[str] = None):
        return self.requests("patch", url, data=data, nested_keys=nested_keys, jsonpath_expr=jsonpath_expr)

    gets = get
    posts = post
    puts = put
    deletes = delete
    patchs = patch

    def is_token_expired(self, response) -> bool:
        return bool(response is not None and response.status_code == 401)
