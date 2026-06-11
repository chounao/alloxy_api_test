import allure
import pytest
import random
import ast
import time
import itertools
from Common.read_and_save_tool import ConfigTools
from api_processor.wallet_model import payee
from api_processor.wallet_model.wallet_list_page import WalletListPage
import Common.assert_tools as assert_tools

# 初始化对象
payee = payee.Payee()
assert_tools = assert_tools.AssertTools()
wallet_list_page = WalletListPage()
config_manager = ConfigTools()









test_crypto_case_name = '钱包-获取加密收款地址列表'
body = {"payee_name":"usdt-bsc","wallet_address":"0x4f563Af4630040afBa824228710Ef454fEddd06f"}
@allure.epic("钱包模块")
@allure.feature("添加收款方流程")
@pytest.mark.parametrize(
    "test_case_name,body",
    [
        (test_crypto_case_name,body)
        # 可在此处添加更多测试组合
    ]
)
def test_get_crypto_payee_data_pass(test_case_name, http_request, body):
    """
    测试获取加密收款地址列表
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :param payee_name: 收款方标识符（用于日志记录等）
    :param wallet_address: 钱包地址（可用于后续校验或其他操作）
    """
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = payee.get_crypto_payee_data(test_case_name, http_request,body)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise








PayeeName_Null_case_name = '钱包-获取加密收款地址列表_PayeeName_Null'
PayeeName_Null_body = {"payee_name":None}
@allure.epic("钱包模块")
@allure.feature("添加收款方流程")
@pytest.mark.parametrize(
    "test_case_name,body",
    [
        (PayeeName_Null_case_name,PayeeName_Null_body)
        # 可在此处添加更多测试组合
    ]
)
def test_get_crypto_payee_data_PayeeName_Null(test_case_name, http_request, body):
    """
    测试获取加密收款地址列表
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :param payee_name: 收款方标识符（用于日志记录等）
    :param wallet_address: 钱包地址（可用于后续校验或其他操作）
    """
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = payee.get_crypto_payee_data(test_case_name, http_request,body)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise








PayeeName_Error_case_name = '钱包-获取加密收款地址列表_PayeeName_Error'
PayeeName_Error_body = {"payee_name":"usdt-bsc-123"}
@allure.epic("钱包模块")
@allure.feature("添加收款方流程")
@pytest.mark.parametrize(
    "test_case_name,body",
    [
        (PayeeName_Error_case_name,PayeeName_Error_body)
        # 可在此处添加更多测试组合
    ]
)
def test_get_crypto_payee_data_PayeeName_Error(test_case_name, http_request, body):
    """
    测试获取加密收款地址列表
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :param payee_name: 收款方标识符（用于日志记录等）
    :param wallet_address: 钱包地址（可用于后续校验或其他操作）
    """
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = payee.get_crypto_payee_data(test_case_name, http_request,body)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise








PayeeName_PUT_SQL_case_name = '钱包-获取加密收款地址列表_PayeeName_PUT_SQL'
PayeeName_PUT_SQL_body = {"payee_name": "1' AND SLEEP(5)--"}
@allure.epic("钱包模块")
@allure.feature("添加收款方流程")
@pytest.mark.parametrize(
    "test_case_name,body",
    [
        (PayeeName_PUT_SQL_case_name,PayeeName_PUT_SQL_body)
        # 可在此处添加更多测试组合
    ]
)
def test_get_crypto_payee_data_PayeeName_PUT_SQL(test_case_name, http_request, body):
    """
    测试获取加密收款地址列表
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :param payee_name: 收款方标识符（用于日志记录等）
    :param wallet_address: 钱包地址（可用于后续校验或其他操作）
    """
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = payee.get_crypto_payee_data(test_case_name, http_request,body)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise








PayeeName_PUT_XSS_case_name = '钱包-获取加密收款地址列表_PayeeName_PUT_XSS'
PayeeName_PUT_XSS_body = {"payee_name":"<script>alert(1)</script>"}
@allure.epic("钱包模块")
@allure.feature("添加收款方流程")
@pytest.mark.parametrize(
    "test_case_name,body",
    [
        (PayeeName_PUT_XSS_case_name,PayeeName_PUT_XSS_body)
        # 可在此处添加更多测试组合
    ]
)
def test_get_crypto_payee_data_PayeeName_PUT_XSS(test_case_name, http_request, body):
    """
    测试获取加密收款地址列表
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :param payee_name: 收款方标识符（用于日志记录等）
    :param wallet_address: 钱包地址（可用于后续校验或其他操作）
    """
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = payee.get_crypto_payee_data(test_case_name, http_request,body)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise








Address_Null_case_name = '钱包-获取加密收款地址列表_Address_Null'
Address_Null_body = {"wallet_address":None}
@allure.epic("钱包模块")
@allure.feature("添加收款方流程")
@pytest.mark.parametrize(
    "test_case_name,body",
    [
        (Address_Null_case_name,Address_Null_body)
        # 可在此处添加更多测试组合
    ]
)
def test_get_crypto_payee_data_Address_Null(test_case_name, http_request, body):
    """
    测试获取加密收款地址列表
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :param payee_name: 收款方标识符（用于日志记录等）
    :param wallet_address: 钱包地址（可用于后续校验或其他操作）
    """
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = payee.get_crypto_payee_data(test_case_name, http_request,body)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise









Address_Error_case_name = '钱包-获取加密收款地址列表_Address_Error'
Address_Error_body = {"wallet_address":"0x4f563Af4630040afBa824228710Ef454fEddd06fssssssss"}
@allure.epic("钱包模块")
@allure.feature("添加收款方流程")
@pytest.mark.parametrize(
    "test_case_name,body",
    [
        (Address_Error_case_name,Address_Error_body)
        # 可在此处添加更多测试组合
    ]
)
def test_get_crypto_payee_data_Address_Error(test_case_name, http_request, body):
    """
    测试获取加密收款地址列表
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :param payee_name: 收款方标识符（用于日志记录等）
    :param wallet_address: 钱包地址（可用于后续校验或其他操作）
    """
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = payee.get_crypto_payee_data(test_case_name, http_request,body)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise












Address_PUT_SQL_case_name = '钱包-获取加密收款地址列表_Address_PUT_SQL'
Address_PUT_SQL_body = {"wallet_address": "1' AND SLEEP(5)--"}
@allure.epic("钱包模块")
@allure.feature("添加收款方流程")
@pytest.mark.parametrize(
    "test_case_name,body",
    [
        (Address_PUT_SQL_case_name,Address_PUT_SQL_body)
        # 可在此处添加更多测试组合
    ]
)
def test_get_crypto_payee_data_Address_PUT_SQL(test_case_name, http_request, body):
    """
    测试获取加密收款地址列表
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :param payee_name: 收款方标识符（用于日志记录等）
    :param wallet_address: 钱包地址（可用于后续校验或其他操作）
    """
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = payee.get_crypto_payee_data(test_case_name, http_request,body)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise








Address_PUT_XSS_case_name = '钱包-获取加密收款地址列表_Address_PUT_XSS'
Address_PUT_XSS_body = {"wallet_address":"<script>alert(1)</script>"}
@allure.epic("钱包模块")
@allure.feature("添加收款方流程")
@pytest.mark.parametrize(
    "test_case_name,body",
    [
        (Address_PUT_XSS_case_name,Address_PUT_XSS_body)
        # 可在此处添加更多测试组合
    ]
)
def test_get_crypto_payee_data_Address_PUT_XSS(test_case_name, http_request, body):
    """
    测试获取加密收款地址列表
    :param test_case_name: 测试用例名称
    :param http_request: HTTP 请求实例
    :param payee_name: 收款方标识符（用于日志记录等）
    :param wallet_address: 钱包地址（可用于后续校验或其他操作）
    """
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = payee.get_crypto_payee_data(test_case_name, http_request,body)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise







test_add_payee_case_name = '钱包-创建提币地址'
currency_list= ['USDT','USDC']
chain_name_list= ['arbitrum','polygon','avalanche','ethereum','bsc']

@allure.epic("钱包模块")
@allure.feature("添加收款方流程")
@pytest.mark.parametrize(
    "test_case_name,payee_name,currency,chain_name",[
        (test_add_payee_case_name,'test_001','USDT','arbitrum'),
        (test_add_payee_case_name,'test_002','USDT','polygon'),
        (test_add_payee_case_name,'test_003','USDT','avalanche'),
        (test_add_payee_case_name,'test_004','USDT','ethereum'),
        (test_add_payee_case_name,'test_005','USDT','bsc'),
        (test_add_payee_case_name,'test_006','USDC','arbitrum'),
        (test_add_payee_case_name,'test_007','USDC','polygon'),
        (test_add_payee_case_name,'test_008','USDC','avalanche'),
        (test_add_payee_case_name,'test_009','USDC','ethereum'),
        (test_add_payee_case_name,'test_010','USDC','bsc')
])
def test_add_crypto_payee_data(test_case_name, http_request, payee_name, currency, chain_name):
    # 测试实现
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = payee.add_payee(test_case_name,http_request,payee_name, currency, chain_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise







test_delete_payee_case_name = '钱包-删除加密收款地址'
@allure.epic("钱包模块")
@allure.feature("删除收款方流程")
@pytest.mark.parametrize(
    "test_case_name,payee_name,currency,chain_name",[
        (test_delete_payee_case_name,'test_001','USDT','arbitrum')
    ])

def test_delete_crypto_payee_data(test_case_name, http_request, payee_name, currency, chain_name):
    # 测试实现
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = payee.delete_payee(test_case_name,http_request,payee_name, currency, chain_name)
            assert_tools._common_response_validation_code(result, test_case_name)
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise








test_get_all_country_info_case_name = '获取所有国家信息'
@allure.epic("钱包模块")
@allure.feature("查询所有国家信息")
def test_get_all_country_info(http_request, test_case_name = test_get_all_country_info_case_name):
    # 测试实现
    with allure.step(f"执行测试: {test_case_name}"):
        try:
            result = payee.get_all_country_data(http_request, test_case_name)
            response, country_list, assert_code, case_id = result
            assert_tools._common_response_validation_code(result, test_case_name)
            #存储起来方便后续 使用
            config_manager.save_value("country_code_list", 'country_list', country_list)

        except AssertionError as e:
            allure.attach(f"断言失败: {str(e)}", name="断言信息")
            raise
        except Exception as e:
            allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
            raise








# 定义本地不支持的国家列表
LOCAL_LIST = ['SGD', 'AED', 'GBP', 'CAD']
# country_code_list = random.sample(ast.literal_eval(config_manager.get_value("country_code_list", 'country_list')), 3)
country_code_list = ast.literal_eval(config_manager.get_value("country_code_list", 'country_list'))
TEST_CASE_NAME = '查询币种支持的银行国家'
@allure.epic("钱包模块")
@allure.feature("查询币种支持的银行国家")
@pytest.mark.parametrize(
    "test_case_name,currency,country_code",
    [
        (TEST_CASE_NAME, currency, country_code)
        for currency in LOCAL_LIST
        for country_code in country_code_list
    ]
)

def test_assert_currency_code(http_request, test_case_name, currency, country_code):
    # 过滤出支持的国家代码

    # 为每个支持的国家执行测试

        with allure.step(f"执行测试: {test_case_name} - 货币:{currency} 国家:{country_code}"):
            try:
                time.sleep(1.5)  # 在API调用前添加延迟
                result = payee.get_foreign_currency_supported_countries(
                    http_request, test_case_name, currency, country_code
                )
                assert_tools._common_response_validation_code(result, test_case_name)

            except AssertionError as e:
                allure.attach(f"断言失败: {str(e)}", name="断言信息")
                raise
            except Exception as e:
                allure.attach(f"测试执行异常: {str(e)}", name="异常信息")
                raise









@allure.epic("钱包模块")
@allure.feature("查询随机国家代码")
@pytest.mark.parametrize(
    "currency, country_code",
    [ ('SGD','SG'), ('AED','AE'), ('GBP','GB'), ('CAD','CA')

    ]
)
def test_get_country_code_list(http_request,currency, country_code):
    """
    获取所有国家代码
    :param http_request:
    :return:
    """
    payee.get_random_country_code(http_request,currency, country_code)












payee_type = ['personal', 'business']
currency_mapping = {'international': ['USD'],
          'local': ['SGD', 'HKD', 'BWP', 'KES', 'MWK', 'NGN', 'RWF', 'ZAR', 'TZS', 'UGX', 'ZMW',
                    'EUR', 'AED', 'GBP', 'CAD', 'EUR','KRW']}

#
# payee_type = ['personal', 'business']
# currency_mapping = {'international': ['USD'],
#           'local': ['HKD',
#                     'SGD', 'AED', 'GBP', 'CAD']}
@allure.epic("钱包模块")
@allure.feature("发送收款方数据")
@pytest.mark.parametrize(
    "payee_type, payment_data",
    [
        (i, [key, currency])
        for i in payee_type
        for key, value in currency_mapping.items()
        for currency in value
    ]
)
def test_send_data(payee_type, payment_data, http_request):
    """
    测试发送数据
    :param payee_type:
    :param payment_data:
    :return:
    """
    body = payee.send_body(payee_type, payment_data, http_request)










# payee_type = ['personal', 'business']
# currency_mapping = {'international': ['USD'],
#           'local': ['SGD', 'HKD',
#                     'EUR', 'AED']}

test_add_payee_bank_account_case_name = '钱包-创建银行收款地址'
@allure.epic("钱包模块")
@allure.feature("添加收款方银行账户")
@pytest.mark.parametrize(
    "test_case_name,payee_type,payment_data",
    [
        (test_add_payee_bank_account_case_name, i, [key, currency])
        for i in payee_type
        for key, value in currency_mapping.items()
        for currency in value
    ]
)
def test_add_payee_bank_account(http_request, test_case_name,payee_type, payment_data):
    """
    测试添加收款方银行账户
    :param test_case_name:
    :param body : 收款方银行账户信息international，
    :return:
    """
    with allure.step(f"执行测试: {test_case_name}"):
        body = payee.send_body(payee_type, payment_data, http_request)
        result = payee.create_payee_bank_account(http_request, test_case_name, body)
        assert_tools._common_response_validation_code(result, test_case_name)




test_add_payee_bank_account_detail_case_name = '钱包-查看银行信息详情'

@allure.epic("钱包模块")
@allure.feature("查看收款方银行账户详情")
@pytest.mark.parametrize(
    "test_case_name",
    [
        (test_add_payee_bank_account_detail_case_name)
    ]
)
def test_get_payee_bank_account_details(test_case_name, http_request):
    """
    测试查看收款方银行账户详情
    :param http_request:
    :return:
    """
    with allure.step(f"执行测试: {test_case_name}"):
        total, id_list= payee.get_payee_bank_account_data( http_request, payee_name = '')
        payee_id = random.choice(id_list)
        result = payee.get_payee_bank_account_details(test_case_name, http_request, payee_id)
        assert_tools._common_response_validation_code(result, test_add_payee_bank_account_detail_case_name)




test_update_payee_bank_account_case_name = '钱包-更新银行收款地址信息'
@allure.epic("钱包模块")
@allure.feature("更新收款方银行账户")
@pytest.mark.parametrize(
    "test_case_name",
    [
        (test_update_payee_bank_account_case_name)
    ]
)
def test_update_payee_bank_account(test_case_name, http_request):
    """
    测试更新收款方银行账户
    :param http_request:
    :return:
    """
    with allure.step(f"执行测试: {test_case_name}"):
        otal, id_list = payee.get_payee_bank_account_data(http_request, payee_name='')
        payee_id = random.choice(id_list)
        result = payee.get_payee_bank_account_details(test_add_payee_bank_account_detail_case_name, http_request, payee_id)
        response, extracted_parameters, assert_code, case_id = result
        result = payee.update_payee_bank_account(test_case_name, http_request, body = extracted_parameters)
        assert_tools._common_response_validation_code(result, test_delete_payee_case_name)



test_delete_payee_bank_case_name = '钱包-删除银行收款地址'
@allure.epic("钱包模块")
@allure.feature("删除收款方银行账户")
@pytest.mark.parametrize(
    "test_case_name",
    [
        (test_delete_payee_bank_case_name)
    ]
)
def test_delete_payee_bank_account(test_case_name, http_request):
    """
    测试删除收款方银行账户
    :param http_request:
    :return:
    """
    with allure.step(f"执行测试: {test_case_name}"):
        total, id_list= payee.get_payee_bank_account_data( http_request, payee_name = '')
        for i in id_list:
            result = payee.delete_payee_bank_account(test_case_name, http_request, i)
            assert_tools._common_response_validation_code(result, test_delete_payee_case_name)




if __name__ == '__main__':
    pytest.main(['-s', 'test_payee.py'])


