#keywords.py
import logging
import time
import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utils.keywords_utils import kw_step


class Keywords:
    """
    把 WebDriver（浏览器对象）作为参数传进来；
    封装所有可复用的浏览器操作；
    提供一个统一接口给测试用例调用。
    """
    def __init__(self, driver):
        self.driver = driver

    # ================== 基础定位方法 ==================
    # def find(self, step):
    #     wait = WebDriverWait(self.driver,10)
    #     locator = step['by'], step['value']
    #
    #     if step["index"] is None:
    #         return wait.until(EC.presence_of_element_located(locator))#只要元素出现在DOM中就定位
    #     else:
    #         return wait.until(EC.presence_of_all_elements_located(locator))[step["index"]]
    def find(self, step):
        """定位元素"""
        wait = WebDriverWait(self.driver, timeout=10)
        locator = step["by"], step["value"]

        try:
            # 如果 index 为 None，则定位单个元素，否则定位一组元素中的某个
            if step["index"] is None:
                return wait.until(EC.presence_of_element_located(locator))
            else:
                return wait.until(EC.presence_of_all_elements_located(locator))[step["index"]]
        except TimeoutException:
            logging.error(f"❌ 元素定位失败，元素定位信息为: {locator}")
            # 抛出异常给上层调用者（例如 assert_element_exist）
            raise
    # ================== 和操作有关的关键字 ==================
    # 每个关键字实际上是对应一个步骤
    @kw_step
    def open(self, step):
        #打开网址
        self.driver.get(step["data"])#每个关键字函数都能通过 self.driver 去控制浏览器；

    @kw_step
    def click(self, step):
        #点击
        self.find(step).click()

    @kw_step
    def input(self, step):
        #输入文本
        self.find(step).send_keys(step["data"])

    @kw_step
    def clear(self, step):
        #清空
        self.find(step).clear()

    @kw_step
    def wait(self, step):
        #等待
        time.sleep(step["data"])

    @kw_step
    def shot(self, step):
        """截图"""
        now_time = time.strftime("%Y-%m-%d %H_%M_%S")
        png = self.driver.get_screenshot_as_png()
        allure.attach(
            png,
            f"第{step['step_num']}步_{now_time}.png",
            allure.attachment_type.PNG
        )

