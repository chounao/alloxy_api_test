import os
import ast
import configparser
import ast
import re
from Common.execute import get_config_section, get_env  # 导入环境工具函数
from Common import logger
logger = logger.logger
class ConfigTools:
    """
    配置文件读取类

    用于读取和解析INI格式的配置文件，支持指定文件路径或使用默认路径

    Args:
        filepath (str, optional): 配置文件路径，如果未指定则使用默认路径
    """
    _instance = None
    _initialized = False

    def __new__(cls, filepath=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, filepath=None):

        # 1. 确定配置文件路径
        if not self._initialized:
            # 原有的初始化逻辑
            if filepath:
                self.configpath = filepath
            else:
                self.configpath = os.path.join(os.path.dirname(__file__), 'config.ini')
            # 2. 检查配置文件是否存在
            if not os.path.exists(self.configpath):
                logger.error(f'配置文件不存在: {self.configpath}')
                raise FileNotFoundError(f'配置文件不存在: {self.configpath}')

            # 3. 读取配置文件
            self.config = configparser.RawConfigParser()
            try:
                self.config.read(self.configpath, encoding='utf-8')
            except Exception as e:
                logger.error(f'配置文件读取失败: {self.configpath}, 错误: {str(e)}')
                raise RuntimeError(f'配置文件读取失败: {self.configpath}, 错误: {str(e)}')
            # 4. 关键：获取当前环境对应的配置节（关联环境变量）

            self.config_section = get_config_section()
            self.current_env = get_env()
            logger.info(f"ConfigTools 初始化完成，当前环境：{self.current_env}，配置节：{self.config_section}")

            self._initialized = True


        self._cached_data = None
        self._config_data = None

        self.api_section = 'API_DATA'


    def get_value(self, section, key):
        """
        通过节名和键名获取配置值

        Args:
            section (str): 配置节名
            key (str): 配置键名

        Returns:
            str: 配置值，如果不存在则返回None
        """
        try:
            # 直接通过section和key获取值
            if self.config.has_section(section) and self.config.has_option(section, key):
                return self.config.get(section, key)
            else:
                return None
        except Exception as e:
            logger.error(f"获取配置值失败: {e}")
            return None

    def save_value(self, section, key, value):
        """
        保存单个配置值到配置文件

        Args:
            section (str): 配置节名
            key (str): 配置键名
            value (str): 配置值
        """
        try:
            # 确保section存在
            if not self.config.has_section(section):
                self.config.add_section(section)
            if not isinstance(key, str):
                key = str(key)
            if not isinstance(value, str):
                value = str(value)
            # 设置值
            self.config.set(section, key, str(value))

            # 保存到文件
            with open(self.configpath, 'w', encoding='utf-8') as configfile:
                self.config.write(configfile)
                logger.info(f"配置已保存到文件: {self.configpath}")

        except Exception as e:
            logger.error(f"保存配置值失败: {e}")
            raise

    def get_section_data(self, section):
        """
        获取整个节的配置数据

        Args:
            section (str): 配置节名

        Returns:
            dict: 节内所有键值对，如果节不存在则返回None
        """
        try:
            if self.config.has_section(section):
                return dict(self.config.items(section))
            else:
                return None
        except Exception as e:
            logger.error(f"获取节数据失败: {e}")
            return None


    def process_url_placeholder(self,url_template, replace_values):
        """
        处理URL模板中的占位符：先提取占位符，再替换为指定值

        参数：
            url_template: 包含占位符的URL模板（如 "https://example.com/{id}"）
            replace_values: 替换值字典（如 {"id": "123"}）

        返回：
            替换后的完整URL字符串
        """
        # 步骤1：提取所有占位符（{...}中的内容）
        pattern = r"\{(.*?)\}"
        placeholders = re.findall(pattern, url_template)

        # 检查替换值是否覆盖所有占位符
        for placeholder in placeholders:
            if placeholder not in replace_values:
                logger.error(f"缺少替换值：URL中的占位符 '{placeholder}' 未在replace_values中找到")
                raise ValueError(f"缺少替换值：URL中的占位符 '{placeholder}' 未在replace_values中找到")

        # 步骤2：替换所有占位符
        processed_url = url_template
        for placeholder, value in replace_values.items():
            # 确保占位符带{}（如将"id"转为"{id}"）
            placeholder_with_braces = f"{{{placeholder}}}"
            processed_url = processed_url.replace(placeholder_with_braces, str(value))
        logger.info(f"URL已处理: {processed_url}")

        return processed_url

    def get_url_method(self,api_name:str =  None,
                       ping_data:str = None,
                       replace_data:str = None,
                       dict_data:dict =None):
        """
        获取请求体URL方法

        Args:
            api_name (str): 配置键名
            ping_data (str): 查询参数
            replace_data (str): 替换参数
            dict_data (dict): 字典参数

            Returns:
                str: URL方法
            """

        authority = self.get_value(section = self.config_section, key = 'URL')
        try:
            url_method = self.get_value(section = self.api_section, key = api_name)
            if url_method:
                # 解析配置值
                parsed_value = ast.literal_eval(url_method)

                method = parsed_value[0]
                url_path = parsed_value[1]

                # replace_data，则格式化URL路径
                if replace_data :
                    #主要是为了解决拿到api内参数的问题https://example.com/{id}替换id这种
                    url_01 = authority + url_path
                    url = self.process_url_placeholder(url_01, replace_data)
                    logger.info(f"URL已处理: {url}")
                elif ping_data:
                    #主要是pin下完整的链接比如 https://example.com?page=1&take=20 查询列表数据操作
                    url = authority + url_path +f'?{ping_data}'
                    logger.info(f"URL已处理: {url}")
                elif dict_data and isinstance(dict_data, dict):
                    # 处理字典形式的查询参数
                    query_params = []
                    for key, value in dict_data.items():
                        if value is None:
                            continue
                            # 处理数组类型的参数，如 create_at[]
                        elif isinstance(value, list):
                            for item in value:
                                # 过滤掉列表中的None值
                                if item is not None:
                                    query_params.append(f"{key}[]={item}")

                        else:
                            query_params.append(f"{key}={value}")

                    url = authority + url_path + "?" + "&".join(query_params)
                    logger.info(f"URL已处理: {url}")

                else:
                    url = authority + url_path

                    logger.info(f"URL已处理: {url}")

                return method, url
            return None
        except Exception as e:
            logger.error(f"获取URL方法失败: {e}")
            return None

    def get_data_from_name(self,api_name:str =  None,
                       ping_data:str = None,
                       replace_data:str = None,
                       dict_data:dict =None):
        """
        获取请求体数据方法

        Args:
            api_name (str): 配置键名
            ping_data (str): 获取参数
            replace_data (str): 替换参数
            dict_data (dict): 字典参数

            Returns:
                str: 数据方法
            """

        return self.get_url_method(api_name=api_name,
                                   ping_data=ping_data,
                                   replace_data=replace_data,
                                   dict_data=dict_data)
    def get_menu_ids(self):
        data = self.get_value(section = 'MENU_ID',key = 'menu_ids')
        data = ast.literal_eval(data)
        logger.info(data)
        return data
    def get_login_data(self,key):
        """
        获取登录数据

        Returns:
            tuple: 登录数据元组，包含用户名和密码
        """
        data = self.get_value(section = self.config_section,key = key)

        return data
    def get_url_data(self):
        """
        获取URL数据

        Returns:
            tuple: URL数据元组，包含URL和请求方法
        """
        return self.get_value(section = self.config_section,key = 'URL')
    def get_access_token(self):
        """
        获取access_token

        Returns:
            str: access_token
        """
        return self.get_value(section = self.config_section,key = 'access_token')


    def get_pay_in_county(self):
        """
        获取支付国家

        Returns:
            str: 支付国家
        """
        data = self.get_value(section = 'PAY_IN_COUNTY',key = 'pay_in_county')
        print(type(data))
        return data

    def get_pay_out_county(self):
        """
        获取支付国家

        Returns:
            str: 支付国家
        """
        data = self.get_value(section = 'PAY_OUT_COUNTY',key = 'pay_out_county')

    def get_common_value(self, section,key,currency, key_name:list[str] = None):
        value_list = []

        value_data = self.get_value(section=section, key=key)
        if value_data is not None and isinstance(value_data, str):
            try:
                data = ast.literal_eval(value_data)
                if isinstance(data, dict):
                    for target_key in key_name:
                        value_list.append(data.get(target_key))
                return value_list
            except (ValueError, SyntaxError) as e:
                logger.error(f"获取{currency}数据失败: {e}")
                return None
        return None
    #获取法币
    def _get_fiat_value(self,currency, key_name:list[str] = None):
        return self.get_common_value('fiat_data',key=f'fiat_{currency}_dict',currency=currency, key_name=key_name)
    #获取虚拟币
    def _get_crypto_value(self,currency, key_name:list[str] = None):
        return self.get_common_value('crypto_data',key = f'crypto_{currency}_dict', currency=currency, key_name=key_name)

    #获取pay_in/pay_out
    def get_yellow_card_data(self, yellow_card_type, get_key_name: list[str] = None):
        """
        获取黄牌数据

        Args:
            yellow_card_type (str): 黄牌类型
            get_key_name (list[str]): 需要获取的键名列表

        Returns:
            list: 按组返回的数据列表，格式为 [[value1_1, value1_2], [value2_1, value2_2], ...]
        """
        if not yellow_card_type or not get_key_name:
            return None

        yellow_card_data = self.get_value(
            section=f'crypto_{yellow_card_type}_data',
            key=f'crypto_{yellow_card_type}_dict'
        )

        if yellow_card_data is not None and isinstance(yellow_card_data, str):
            try:
                data = ast.literal_eval(yellow_card_data)
                if isinstance(data, dict):
                    result_list = []

                    # 遍历数据字典
                    for key, value in data.items():
                        # 如果value是字典，提取指定键的值
                        if isinstance(value, dict):
                            row_data = []
                            for target_key in get_key_name:
                                row_data.append(value.get(target_key, None))
                            result_list.append(row_data)
                        # 如果value是列表，遍历列表元素
                        elif isinstance(value, list):
                            for item in value:
                                if isinstance(item, dict):
                                    row_data = []
                                    for target_key in get_key_name:
                                        row_data.append(item.get(target_key, None))
                                    result_list.append(row_data)
                    return result_list
                return None
            except (ValueError, SyntaxError) as e:
                logger.error(f"获取{yellow_card_type}数据失败: {e}")
                return None
        return None


# 创建全局实例供其他模块使用
configtools = ConfigTools()

if __name__ == '__main__':
    read_config = ConfigTools()
    # value =read_config._get_crypto_value('usdt',['currency','decimal_calculate_places'])
    # data  = read_config._get_fiat_value('TZS',['decimal_places','decimal_calculate_places'])
    # print(value)
    # print(data)
    read_config.get_menu_ids()