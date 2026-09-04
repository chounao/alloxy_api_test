import json
import re
from copy import deepcopy
from typing import Any, Mapping, Optional


class DataResolveError(ValueError):
    """测试数据变量解析失败时抛出的异常。"""


class DataResolver:
    """Excel 请求体变量解析工具。

    中文备注：用于把 Excel 请求体中的 ${变量名} 替换为运行时变量，支持 dict/list/str
    递归替换，适合 wallet_id、payee_id、department_id 等前置数据注入场景。
    """

    VARIABLE_PATTERN = re.compile(r"\$\{([^}]+)}")

    @classmethod
    def parse_json_object(cls, raw_body: Any) -> dict:
        """把 Excel 请求体解析为 dict。

        中文备注：请求体为空时返回空 dict；请求体必须是 JSON 对象，不建议 Excel 中维护
        顶层数组，否则后续变量合并和 Allure 展示都不稳定。
        """
        if raw_body is None or raw_body == "":
            return {}
        if isinstance(raw_body, dict):
            return deepcopy(raw_body)
        if isinstance(raw_body, str):
            try:
                parsed = json.loads(raw_body)
            except json.JSONDecodeError as exc:
                raise DataResolveError(f"请求体不是合法JSON: {exc.msg}; 内容: {raw_body}") from exc
            if parsed is None:
                return {}
            if not isinstance(parsed, dict):
                raise DataResolveError(f"请求体顶层必须是JSON对象，实际为: {type(parsed).__name__}")
            return parsed
        raise DataResolveError(f"不支持的请求体类型: {type(raw_body).__name__}")

    @classmethod
    def resolve(cls, data: Any, variables: Optional[Mapping[str, Any]] = None, strict: bool = True) -> Any:
        """递归替换变量。

        Args:
            data: dict/list/str/int/float/bool/None 任意请求数据。
            variables: 变量池，如 {"wallet_id": "xxx"}。
            strict: True 时遇到缺失变量直接抛错；False 时保留原占位符。
        """
        variables = variables or {}
        if isinstance(data, dict):
            return {cls.resolve(key, variables, strict): cls.resolve(value, variables, strict)
                    for key, value in data.items()}
        if isinstance(data, list):
            return [cls.resolve(item, variables, strict) for item in data]
        if isinstance(data, tuple):
            return tuple(cls.resolve(item, variables, strict) for item in data)
        if isinstance(data, str):
            return cls._resolve_string(data, variables, strict)
        return data

    @classmethod
    def merge_and_resolve(
        cls,
        raw_body: Any,
        variables: Optional[Mapping[str, Any]] = None,
        override: Optional[Mapping[str, Any]] = None,
        strict: bool = True,
    ) -> dict:
        """解析 Excel 请求体、替换变量、合并额外覆盖参数。

        中文备注：推荐业务层只传入变量池，不再手动拼 JSON；确实需要临时覆盖字段时，
        使用 override 覆盖最终请求体字段。
        """
        body = cls.parse_json_object(raw_body)
        resolved = cls.resolve(body, variables, strict)
        if override:
            if not isinstance(override, Mapping):
                raise TypeError("override必须是Mapping类型")
            resolved.update(dict(override))
        return resolved

    @classmethod
    def _resolve_string(cls, text: str, variables: Mapping[str, Any], strict: bool) -> Any:
        matches = cls.VARIABLE_PATTERN.findall(text)
        if not matches:
            return text

        # 中文备注：整个字符串只有一个变量时，保留变量原始类型，如 int/bool/dict。
        if len(matches) == 1 and text == f"${{{matches[0]}}}":
            key = matches[0]
            if key not in variables:
                if strict:
                    raise DataResolveError(f"变量未提供: {key}")
                return text
            return variables[key]

        result = text
        for key in matches:
            if key not in variables:
                if strict:
                    raise DataResolveError(f"变量未提供: {key}")
                continue
            result = result.replace(f"${{{key}}}", str(variables[key]))
        return result
