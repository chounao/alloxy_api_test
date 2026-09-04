import json
from typing import Any, Iterable, Optional

import allure
import pytest
from jsonpath_ng.ext import parse


class ResponseAssertionError(AssertionError):
    """响应断言失败。"""


class ResponseAssertion:
    """配置化响应断言工具。

    中文备注：用于支持 Excel 配置 JSONPath、断言方式和预期值，减少测试代码中的
    手写 assert，让接口断言数据驱动化。
    """

    @staticmethod
    def extract(response_json: dict, jsonpath_expr: str):
        matches = [match.value for match in parse(jsonpath_expr).find(response_json)]
        if len(matches) == 1:
            return matches[0]
        return matches

    @classmethod
    def assert_by_rule(cls, actual: Any, operator: str, expected: Any = None) -> None:
        operator = (operator or "equals").strip().lower()
        if operator == "equals":
            assert actual == expected, f"期望等于 {expected!r}，实际 {actual!r}"
        elif operator == "not_empty":
            assert actual not in (None, "", [], {}), f"期望非空，实际 {actual!r}"
        elif operator == "contains":
            assert expected in actual, f"期望 {actual!r} 包含 {expected!r}"
        elif operator == "not_contains":
            assert expected not in actual, f"期望 {actual!r} 不包含 {expected!r}"
        elif operator == "greater_than":
            assert float(actual) > float(expected), f"期望 {actual!r} 大于 {expected!r}"
        elif operator == "less_than":
            assert float(actual) < float(expected), f"期望 {actual!r} 小于 {expected!r}"
        elif operator == "in":
            assert actual in expected, f"期望 {actual!r} 在 {expected!r} 中"
        else:
            raise ValueError(f"不支持的断言方式: {operator}")

    @classmethod
    def assert_response_rules(cls, response, rules: Optional[Iterable[dict]]) -> None:
        """执行多条响应断言规则。

        rule 示例：
            {"jsonpath": "$.data.id", "operator": "not_empty"}
            {"jsonpath": "$.code", "operator": "equals", "expected": 0}
        """
        if not rules:
            return

        try:
            response_json = response.json()
        except ValueError as exc:
            pytest.fail(f"响应体不是合法JSON，无法执行JSONPath断言: {exc}")
            return

        allure.attach(
            json.dumps(list(rules), ensure_ascii=False, indent=2),
            name="配置化断言规则",
            attachment_type=allure.attachment_type.JSON,
        )

        for index, rule in enumerate(rules, start=1):
            jsonpath_expr = rule.get("jsonpath")
            operator = rule.get("operator", "equals")
            expected = rule.get("expected")
            with allure.step(f"响应断言 {index}: {jsonpath_expr} {operator}"):
                actual = cls.extract(response_json, jsonpath_expr)
                try:
                    cls.assert_by_rule(actual, operator, expected)
                except AssertionError as exc:
                    allure.attach(
                        json.dumps({"actual": actual, "expected": expected}, ensure_ascii=False, indent=2),
                        name="断言失败上下文",
                        attachment_type=allure.attachment_type.JSON,
                    )
                    raise ResponseAssertionError(str(exc)) from exc
