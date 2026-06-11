
import os
import Common.logger
logger = Common.logger.logger

# _current_env = "test"  # 默认环境
# _current_config_section = "TEST_CONFIG"  # 默认配置节
_current_env = "test"  # 默认环境
_current_config_section = "TEST_CONFIG"  # 默认配置节
def set_env(env):
    """
    设置环境，通过设置自动切换环境
    """
    global _current_env, _current_config_section

    env = env.lower().strip()  # 处理大小写和空格

    # 环境与配置节的映射关系（用字典替代冗长的 if-elif）
    env_mapping = {
        "test": "TEST_CONFIG",
        "uat": "UAT_CONFIG",
        "prod": "PROD_CONFIG"
    }

    if env not in env_mapping:
        raise ValueError(f"无效环境：{env}，请使用 test/uat/prod")

    # 更新全局变量和系统环境变量
    _current_env = env
    _current_config_section = env_mapping[env]
    os.environ["APP_ENV"] = env  # 供其他模块读取

    logger.info(f"环境已切换至：{env}（配置节：{_current_config_section}）")
    return _current_config_section

def get_env() -> str:
    """获取当前环境名称（test/uat/prod）"""
    return _current_env


def get_config_section() -> str:
    """获取当前环境对应的配置节名称"""
    return _current_config_section



# 默认初始化
# set_envtext = 'test'
# set_env(set_envtext)
# logger = Common.logger.logger
# logger.info(f"---测试开始---执行的是{set_envtext}环境")
