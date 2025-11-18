#keywords.py
import logging
import time
import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
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

    # ================== 浏览器基本操作 ==================
    @kw_step
    def refresh(self, step):
        """刷新当前页面"""
        self.driver.refresh()

    @kw_step
    def back(self, step):
        """浏览器后退"""
        self.driver.back()

    @kw_step
    def forward(self, step):
        """浏览器前进"""
        self.driver.forward()

    @kw_step
    def switch_to_window(self, step):
        """ 根据窗口句柄索引切换窗口"""
        handlers = self.driver.window_handles
        # handlers[step["data"]]  根据索引取句柄
        self.driver.switch_to_window(handlers[step["data"]])

    # ================== 下拉框操作 ==================
    @kw_step
    def select_by_text(self, step):
        """
        通过可见文本选择下拉框选项
        step['data']：要选择的文本
        """
        element = self.find(step)
        Select(element).select_by_visible_text(str(step["data"]))

    @kw_step
    def select_by_value(self, step):
        """
        通过 value 值选择下拉框选项
        step['data']：option 的 value
        """
        element = self.find(step)
        Select(element).select_by_value(str(step["data"]))

    # ================== 弹出框操作（alert） ==================
    @kw_step
    def alert_accept(self, step):
        """接受 alert 弹窗"""
        alert = self.driver.switch_to.alert
        alert.accept()

    @kw_step
    def alert_dismiss(self, step):
        """取消 / 关闭 alert 弹窗"""
        alert = self.driver.switch_to.alert
        alert.dismiss()

    # ================== 滚动条 & JS 操作 ==================
    @kw_step
    def scroll_to(self, step):
        """
        滚动到某个绝对坐标位置
        step['data'] 数据要写成 {'x': 100, 'y': 100} 的形式
        """
        # 这里 eval() 函数是把字符串转换成字典
        position_dict = eval(step["data"])

        js = f"window.scrollTo({position_dict['x']}, {position_dict['y']});"
        self.driver.execute_script(js)

    @kw_step
    def execute_js(self, step):
        self.driver.execute_script(step['data'])


    # ================== 鼠标 & 键盘常用交互 ==================
    @kw_step
    def double_click(self, step):
        """双击"""
        element = self.find(step)
        action = ActionChains(self.driver)#初始化一个“鼠标动作链”对象，把浏览器驱动 driver 传进去，之后的鼠标操作都要通过它来执行
        action.double_click(element).perform()

    @kw_step
    def right_click(self, step):
        """右击"""
        element = self.find(step)
        action = ActionChains(self.driver)
        action.context_click(element).perform()

    @kw_step
    def hover(self, step):
        """悬停"""
        element = self.find(step)
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()

    @kw_step
    def drag_and_drop(self, step):
        source = self.find(step)
        """拖拽
        step['data'] 数据要写成 {'by': xpath, 'value': 'xxx'} 的形式"""
        # 这里 eval() 函数是把字符串转换成字典
        target_dict = eval(step["data"])
        target = self.driver.find_element(target_dict["by"], target_dict["value"])
        action = ActionChains(self.driver)
        action.drag_and_drop(source, target).perform()

    @kw_step
    def enter(self, step):
        """回车"""
        element = self.find(step)
        element.send_keys(Keys.ENTER)