import ast
import configparser
import os
import re
from pathlib import Path
from typing import Any, Dict, Iterable, Optional
from urllib.parse import urlencode

from Common import logger
from Common.execute import get_config_section, get_env


logger = logger.logger


class ConfigTools:
    """INI 配置读取工具。

    中文备注：运行时动态读取 Common.execute 中的当前环境，避免 import 阶段单例缓存
    导致 pytest --env=test/uat/prod 切换不生效。
    """

    def __init__(self, filepath: Optional[str] = None):
        self.configpath = Path(filepath or Path(__file__).resolve().parent / "config.ini")
        if not self.configpath.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.configpath}")
        self.config = configparser.RawConfigParser()
        self.reload()
        self.api_section = "API_DATA"

    @property
    def config_section(self) -> str:
        return get_config_section()

    @property
    def current_env(self) -> str:
        return get_env()

    def reload(self) -> None:
        read_files = self.config.read(self.configpath, encoding="utf-8")
        if not read_files:
            raise RuntimeError(f"配置文件读取失败: {self.configpath}")

    def get_value(self, section: str, key: str, default=None):
        if not self.config.has_section(section):
            logger.warning("配置节不存在: %s", section)
            return default
        if not self.config.has_option(section, key):
            logger.warning("配置项不存在: [%s] %s", section, key)
            return default
        return self.config.get(section, key)

    def save_value(self, section: str, key: str, value: Any) -> None:
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, str(key), str(value))
        with self.configpath.open("w", encoding="utf-8") as configfile:
            self.config.write(configfile)
        logger.info("配置已保存: [%s] %s", section, key)

    def get_section_data(self, section: str) -> Optional[dict]:
        if not self.config.has_section(section):
            return None
        return dict(self.config.items(section))

    def _literal(self, value: str, name: str):
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError) as exc:
            raise ValueError(f"配置{name}不是合法Python字面量: {value}") from exc

    def process_url_placeholder(self, url_template: str, replace_values: Optional[dict]) -> str:
        replace_values = replace_values or {}
        placeholders = re.findall(r"\{(.*?)}", url_template)
        missing = [item for item in placeholders if item not in replace_values]
        if missing:
            raise ValueError(f"URL占位符缺少替换值: {missing}")
        url = url_template
        for key, value in replace_values.items():
            url = url.replace(f"{{{key}}}", str(value))
        return url

    def _encode_query(self, dict_data: Optional[dict]) -> str:
        # 中文备注：使用 urlencode 统一处理中文、空格、特殊字符和列表参数。
        if not dict_data:
            return ""
        pairs = []
        for key, value in dict_data.items():
            if value is None:
                continue
            if isinstance(value, (list, tuple, set)):
                pairs.extend((f"{key}[]", item) for item in value if item is not None)
            else:
                pairs.append((key, value))
        return urlencode(pairs, doseq=True)

    def get_url_method(self, api_name: str = None, ping_data: str = None,
                       replace_data: dict = None, dict_data: dict = None):
        # 中文备注：根据 API_DATA 中的接口名称组装 method 和完整 URL。
        if not api_name:
            raise ValueError("api_name不能为空")

        authority = (self.get_value(self.config_section, "URL") or "").rstrip("/")
        raw = self.get_value(self.api_section, api_name)
        if raw is None:
            raise KeyError(f"API_DATA未配置接口: {api_name}")

        parsed = self._literal(raw, api_name)
        if not isinstance(parsed, (list, tuple)) or len(parsed) < 2:
            raise ValueError(f"API配置格式错误，应为['method', '/path']: {api_name}={raw}")

        method = str(parsed[0]).lower()
        path = str(parsed[1])
        path = path if path.startswith("/") else f"/{path}"
        url = f"{authority}{path}"

        if replace_data:
            url = self.process_url_placeholder(url, replace_data)
        if ping_data:
            url = f"{url}?{ping_data.lstrip('?')}"
        else:
            query = self._encode_query(dict_data)
            if query:
                url = f"{url}?{query}"

        logger.info("URL已处理: %s %s", method.upper(), url)
        return method, url

    def get_data_from_name(self, api_name: str = None, ping_data: str = None,
                           replace_data: dict = None, dict_data: dict = None):
        return self.get_url_method(api_name=api_name, ping_data=ping_data,
                                   replace_data=replace_data, dict_data=dict_data)

    def get_menu_ids(self):
        return self._literal(self.get_value("MENU_ID", "menu_ids", "[]"), "menu_ids")

    def get_login_data(self, key: str):
        return self.get_value(self.config_section, key)

    def get_url_data(self):
        return self.get_value(self.config_section, "URL")

    def get_access_token(self):
        return self.get_value(self.config_section, "access_token")

    def get_pay_in_county(self):
        return self._literal(self.get_value("PAY_IN_COUNTY", "pay_in_county", "{}"), "pay_in_county")

    def get_pay_out_county(self):
        return self._literal(self.get_value("PAY_OUT_COUNTY", "pay_out_county", "{}"), "pay_out_county")

    def get_common_value(self, section: str, key: str, currency: str, key_name: Iterable[str] = None):
        value_data = self.get_value(section=section, key=key)
        if not value_data:
            return None
        data = self._literal(value_data, f"{section}.{key}")
        if not isinstance(data, dict):
            return None
        if not key_name:
            return data
        return [data.get(target_key) for target_key in key_name]

    def _get_fiat_value(self, currency, key_name: list[str] = None):
        return self.get_common_value("fiat_data", f"fiat_{currency}_dict", currency, key_name)

    def _get_crypto_value(self, currency, key_name: list[str] = None):
        return self.get_common_value("crypto_data", f"crypto_{currency}_dict", currency, key_name)

    def get_yellow_card_data(self, yellow_card_type, get_key_name: list[str] = None):
        if not yellow_card_type or not get_key_name:
            return None
        raw = self.get_value(
            section=f"crypto_{yellow_card_type}_data",
            key=f"crypto_{yellow_card_type}_dict",
        )
        if not raw:
            return None
        data = self._literal(raw, yellow_card_type)
        if not isinstance(data, dict):
            return None

        result_list = []
        for value in data.values():
            records = value if isinstance(value, list) else [value]
            for item in records:
                if isinstance(item, dict):
                    result_list.append([item.get(target_key) for target_key in get_key_name])
        return result_list
