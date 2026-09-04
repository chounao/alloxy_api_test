import json
import os
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Iterable, Optional
from urllib.parse import urlencode

import openpyxl

from Common import logger
from Common.data_resolver import DataResolver
from Common.read_and_save_tool import ConfigTools


logger = logger.logger


class ExcelCaseError(RuntimeError):
    """Excel 用例数据缺失或格式异常时抛出的业务异常。"""


class ExcelTools:
    REQUIRED_COLUMNS = ("用例名称", "请求方法", "接口路径", "预期状态码")

    def __init__(self, file_path: Optional[str] = None):
        self.file_path = Path(file_path or self._get_file_path())
        self.workbook = None
        self.config = ConfigTools()
        self._load_workbook()

    def _get_file_path(self) -> str:
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "api_testcase.xlsx")

    def _load_workbook(self) -> None:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Excel用例文件不存在: {self.file_path}")
        try:
            self.workbook = openpyxl.load_workbook(self.file_path, data_only=True)
        except Exception as exc:
            logger.exception("加载Excel用例文件失败: %s", self.file_path)
            raise ExcelCaseError(f"加载Excel用例文件失败: {self.file_path}") from exc

    def get_sheet(self, sheet_name: str):
        if not sheet_name:
            raise ValueError("sheet_name不能为空")
        if self.workbook is None:
            self._load_workbook()
        if sheet_name not in self.workbook.sheetnames:
            raise ExcelCaseError(
                f"工作表不存在: {sheet_name}; 可用工作表: {', '.join(self.workbook.sheetnames)}"
            )
        return self.workbook[sheet_name]

    def _headers(self, sheet) -> Dict[str, int]:
        # 中文备注：读取并校验表头，提前发现 Excel 模板变更导致的执行异常。
        headers: Dict[str, int] = {}
        for index, cell in enumerate(sheet[1], start=1):
            title = str(cell.value).strip() if cell.value is not None else ""
            if not title:
                continue
            if title in headers:
                raise ExcelCaseError(f"{sheet.title}存在重复表头: {title}")
            headers[title] = index

        missing = [name for name in self.REQUIRED_COLUMNS if name not in headers]
        if missing:
            raise ExcelCaseError(f"{sheet.title}缺少必要表头: {missing}")
        return headers

    def get_row_data_by_test_case_name(self, sheet_name: str, test_case_name: str) -> Dict[str, Any]:
        # 中文备注：只按“用例名称”列精确匹配，避免整行任意单元格误匹配。
        if not test_case_name:
            raise ValueError("test_case_name不能为空")

        sheet = self.get_sheet(sheet_name)
        headers = self._headers(sheet)
        case_col = headers["用例名称"]

        for row_idx in range(2, sheet.max_row + 1):
            case_name = sheet.cell(row=row_idx, column=case_col).value
            if str(case_name).strip() == str(test_case_name).strip():
                return {
                    title: sheet.cell(row=row_idx, column=col_idx).value
                    for title, col_idx in headers.items()
                }

        raise ExcelCaseError(f"未找到用例: sheet={sheet_name}, case={test_case_name}")

    def get_case_data(self, sheet_name: str, test_case_name: str) -> Dict[str, Any]:
        raw = self.get_row_data_by_test_case_name(sheet_name, test_case_name)
        case_data = dict(raw)
        case_data["用例ID"] = raw.get("用例 ID") or raw.get("用例ID")
        case_data["用例结果"] = raw.get("执行结果")
        return case_data

    def write_result(self, sheet_name: str, test_case_name: str, header_title: str, result_data: Any) -> None:
        sheet = self.get_sheet(sheet_name)
        headers = self._headers(sheet)
        if header_title not in headers:
            raise ExcelCaseError(f"{sheet_name}未找到结果列: {header_title}")

        case_col = headers["用例名称"]
        target_row = None
        for row_idx in range(2, sheet.max_row + 1):
            if str(sheet.cell(row=row_idx, column=case_col).value).strip() == str(test_case_name).strip():
                target_row = row_idx
                break
        if target_row is None:
            raise ExcelCaseError(f"写入结果失败，未找到用例: {test_case_name}")

        sheet.cell(row=target_row, column=headers[header_title], value=result_data)
        self.workbook.save(self.file_path)

    def process_url_placeholder(self, url_template: str, replace_values: Optional[dict]) -> str:
        replace_values = replace_values or {}
        placeholders = re.findall(r"\{(.*?)}", url_template)
        missing = [name for name in placeholders if name not in replace_values]
        if missing:
            raise ValueError(f"URL占位符缺少替换值: {missing}")

        url = url_template
        for key, value in replace_values.items():
            url = url.replace(f"{{{key}}}", str(value))
        return url

    def get_url(
        self,
        path: str,
        ping_data: Optional[str] = None,
        replace_data: Optional[dict] = None,
        dict_data: Optional[dict] = None,
    ) -> str:
        if not path:
            raise ValueError("接口路径不能为空")
        authority = (self.config.get_url_data() or "").rstrip("/")
        full_path = path if path.startswith("/") else f"/{path}"
        url = f"{authority}{full_path}"

        if replace_data:
            url = self.process_url_placeholder(url, replace_data)
        if ping_data:
            return f"{url}?{ping_data.lstrip('?')}"
        if dict_data:
            query = self._encode_query(dict_data)
            return f"{url}?{query}" if query else url
        return url

    def _encode_query(self, query_data: Dict[str, Any]) -> str:
        # 中文备注：统一编码查询参数，避免手动拼接导致的特殊字符传参错误。
        normalized = []
        for key, value in query_data.items():
            if value is None:
                continue
            if isinstance(value, (list, tuple, set)):
                normalized.extend((f"{key}[]", item) for item in value if item is not None)
            else:
                normalized.append((key, value))
        return urlencode(normalized, doseq=True)

    def _parse_body(self, body: Any) -> Dict[str, Any]:
        # 中文备注：Excel 中请求体允许为空或 JSON 对象字符串，不允许数组/非法 JSON 混入。
        return DataResolver.parse_json_object(body)

    def _merge_variables(self, body: Dict[str, Any], variables: Optional[dict]) -> Dict[str, Any]:
        # 中文备注：先递归替换 ${变量名}，再把 variables 作为最终字段覆盖，兼容旧写法。
        resolved = DataResolver.resolve(body, variables, strict=False)
        if variables:
            if not isinstance(variables, dict):
                raise TypeError("variables必须是dict")
            resolved.update(variables)
        return resolved

    def update_test_case_result(
        self,
        sheet_name: str,
        test_case_name: str,
        variables: Optional[dict] = None,
        ping_data: Optional[str] = None,
        replace_data: Optional[dict] = None,
        dict_data: Optional[dict] = None,
    ):
        case_data = self.get_case_data(sheet_name, test_case_name)
        method = str(case_data.get("请求方法") or "").strip().lower()
        path = case_data.get("接口路径")
        assert_code = case_data.get("预期状态码")
        case_id = case_data.get("用例ID")

        if not method:
            raise ExcelCaseError(f"{test_case_name}缺少请求方法")
        if assert_code is None:
            raise ExcelCaseError(f"{test_case_name}缺少预期状态码")

        request_body = self._merge_variables(self._parse_body(case_data.get("请求体（JSON）")), variables)
        url = self.get_url(path, ping_data=ping_data, replace_data=replace_data, dict_data=dict_data)
        logger.info("用例数据准备完成: sheet=%s case=%s method=%s url=%s", sheet_name, test_case_name, method, url)
        return method, url, request_body, int(assert_code), case_id

    def close(self) -> None:
        if self.workbook:
            self.workbook.close()
            self.workbook = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
