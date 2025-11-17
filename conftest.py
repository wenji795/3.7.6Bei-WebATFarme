import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


#Fixture 就是可复用的“测试前置与清理”（setup/teardown）或测试数据，pytest 会按名字自动注入到测试里。
#用来干嘛？
#准备资源：浏览器驱动、数据库连接、API 客户端、临时文件夹等
#自动清理：测试结束后关闭浏览器、断开连接、删除临时数据
#共享状态：按范围（scope）控制复用次数，避免重复创建
#提供数据/配置：把测试数据、环境配置用统一入口提供给用例
#依赖组合：一个 fixture 可以依赖另一个 fixture
from utils.driver_utils import get_chrome_driver




#driver_handler → fixture 返回的 driver 对象 → 交给 Keywords → 控制浏览器。
@pytest.fixture(scope="function")
def driver_handler():
    driver = get_chrome_driver()
    yield driver
    driver.quit()


# pytest_runtest_makereport 是 pytest 内置钩子函数，
# 自动执行，用于生成测试用例的执行结果（skipped / passed / failed）
# 常用 @pytest.hookimpl(hookwrapper=True)，表示可以前后夹击（自定义修改）
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    :param item:  测试用例对象本身，包含测试类 / 参数化信息 / 标记 / 所在文件路径等
    :param call:  测试用例执行过程信息，包含执行阶段、执行开始时间、执行结果等
    """
    outcome = yield # 必须通过 yield 获取原始流程的结果，存在outcome中
    res = outcome.get_result() # 再拿到结果的内容，存到res
    # 可以通过打印观察下钩子函数的执行效果
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", res)

    # 如果执行过程中发现执行失败
    if res.when == "call" and res.failed:
        params = item.funcargs # 从测试用例对象获取所有参数
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!params: ", params)
        # 获取 fixture 中的 driver_handler 驱动对象
        driver = params["driver_handler"]
        # 生成当前时间用于命名截图
        now_time = time.strftime("%Y-%m-%d_%H_%M_%S")
        # 截图并按照用例 id 和步骤命名
        driver.save_screenshot(
            f"./screenshot/失败用例_{params['case']['id']}_{params['case']['title']}_{now_time}.png"
        )

