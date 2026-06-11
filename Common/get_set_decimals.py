import math
from Common import read_and_save_tool
import Common.logger as logger
config = read_and_save_tool.ConfigTools()
logger = logger.logger

class Decimals:
    def get_decimals_for_fiat(self,currency):
        """
        获取token的小数位数
        """
        data = config._get_fiat_value(currency, key_name=['currency','decimal_calculate_places','min_increment'])
        if data is None:
            return None

        currency,decimal_calculate_places,min_increment = data
        return currency,decimal_calculate_places,min_increment


    def get_decimals_for_crypto(self, currency):

        data = config._get_crypto_value(currency, key_name=['currency', 'decimal_calculate_places', 'min_increment'])
        if data is None:
            return None

        currency, decimal_calculate_places, min_increment = data
        return currency,decimal_calculate_places,min_increment




    #输入数字和一个带有小数点的参数，根据数字截取小数位数，返回截取后的小数位数
    def truncate_decimal_places(self, number, decimal_str):
        """
        根据指定数字截取小数位数，返回截取后的完整数值

        Args:
            number (int): 要保留的小数位数
            decimal_str (str or float): 包含小数点的数值字符串或浮点数

        Returns:
            str: 截取后的完整数值字符串

        Raises:
            ValueError: 当输入参数无效时抛出异常
            TypeError: 当参数类型不正确时抛出异常
        """
        try:
            # 参数类型检查
            if not isinstance(number, int) or number < 0:
                raise ValueError("number参数必须是非负整数")

            # 转换decimal_str为字符串进行处理
            decimal_string = str(decimal_str)

            # 处理特殊情况：输入为0或0.0等形式
            if decimal_string in ['0', '0.0', '0.00', '0.000', '0.0000', '0.00000', '0.000000', '0.0000000', '0.00000000', '0.000000000', '0.0000000000', '0.00000000000', '0.000000000000', '0.0000000000000', '0.00000000000000', '0.000000000000000']:
                if number == 0:
                    return '0'
                else:
                    return f'0.{"0" * number}'

            # 检查是否包含小数点
            if '.' not in decimal_string:
                # 整数情况，直接返回
                return decimal_string

            # 分离整数部分和小数部分
            parts = decimal_string.split('.')
            integer_part = parts[0]
            decimal_part = parts[1]

            # 根据指定位数截取小数部分
            truncated_decimal = decimal_part[:number] if number < len(decimal_part) else decimal_part

            # 组合返回结果
            if number == 0:
                # 如果要求0位小数，只返回整数部分
                return integer_part
            elif truncated_decimal:
                return f"{integer_part}.{truncated_decimal}"
            else:
                # 小数部分为空时，根据要求的位数补0
                return f"{integer_part}.{'0' * number}"

        except Exception as e:
            raise ValueError(f"处理小数位数时发生错误: {str(e)}")

    #输入数字，根据字数四舍五入小数位
    def round_decimals_for_number(self, number, decimal_places):
        """
        对数字进行四舍五入，保留指定小数位数
        """
        rounded_number = round(number, decimal_places)
        return rounded_number



    # 自定义舍入规则：小数点后第n位不为0则进位，为0则舍去
    def custom_round(self, value, decimal_places):
        """
        自定义舍入规则：小数点后第n位不为0则进位，为0则舍去
        """
        # 输入验证
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                raise TypeError("value must be a number or numeric string")
        if not isinstance(value, (int, float)):
            raise TypeError("value must be a number")

        # 处理特殊值
        if math.isnan(value) or math.isinf(value):
            return value

        try:
            # 计算需要放大的倍数
            multiplier = 10 ** decimal_places
            multiplied = value * multiplier

            # 获取决定舍入的小数位（即第 decimal_places+1 位）
            check_digit_position = decimal_places + 1
            check_multiplier = 10 ** check_digit_position
            check_digit = int((value * check_multiplier) % 10)

            # 根据自定义规则执行舍入
            if check_digit != 0:
                return math.ceil(multiplied) / multiplier
            else:
                return math.floor(multiplied) / multiplier
        except Exception as e:
            raise RuntimeError(f"Error during rounding operation: {e}")



    #截取虚拟币的小数位数
    def _get_decimals_for_crypto(self, currency,decimal_str):
        """
        获取虚拟币的小数位数
        """
        data = self.get_decimals_for_crypto(currency)
        if data is None:
            return None

        currency, decimal_calculate_places, min_increment = data
        decimal_places  = self.truncate_decimal_places(number = decimal_calculate_places, decimal_str = decimal_str)
        logger.info(f"{currency}的截取小数位数为：{decimal_places}")
        return decimal_places
    #截取法币的小数位
    def _get_decimals_for_fiat(self, currency,decimal_str):
        """
        获取法币的小数位数
        """
        data = self.get_decimals_for_fiat(currency)
        if data is None:
            return None

        currency, decimal_calculate_places, min_increment = data
        decimal_places  = self.truncate_decimal_places(number = decimal_calculate_places, decimal_str = decimal_str)
        logger.info(f"{currency}的截取小数位数为：{decimal_places}")
        return decimal_places

if __name__ == '__main__':
    decimals = Decimals()
    decimals._get_decimals_for_crypto('USDT','2.11969845894')
