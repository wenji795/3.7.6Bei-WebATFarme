from core.keywords import Keywords
from utils.keywords_utils import kw_step
import logging

class AssertKeywords(Keywords): #继承Keywords类
    # ================== 和断言有关的关键字 ==================
    @kw_step
    def assert_url(self, step):
        """URL 断言：实际 URL 要包含预期的片段"""
        expected_url = step["data"]            # Excel 里写的期望值
        actual_url = self.driver.current_url   # 浏览器当前的 URL
        # 不包含就抛 AssertionError，pytest 会标红
        assert expected_url in actual_url, f"❌ 当前URL: {actual_url} 不包含 预期URL: {expected_url}"#断言结果是true, 继续往下执行输出日志。false就输出f"❌ 当前URL: {actual_url} 不包含 预期URL: {expected_url}"
        logging.info(f"✅ 当前URL: {actual_url} 包含 预期URL: {expected_url}")

    @kw_step
    def assert_title(self, step):
        """title 断言：实际 title 要包含预期的片段"""
        expected_title = step["data"]
        actual_title = self.driver.title
        assert expected_title in actual_title, f"❌ 当前title: {actual_title} 不包含 预期title: {expected_title}"

    @kw_step
    def assert_text(self, step):
        """text 断言：实际 text 要包含预期的片段"""
        expected_text = step["data"]
        actual_text = self.find(step).text
        assert expected_text in actual_text, f"❌ 当前text: {actual_text} 不包含 预期text: {expected_text}"

    @kw_step
    def assert_alert_text(self, step):
        alert = self.driver.switch_to.alert  # 切换到 alert 对象
        expected_text = step['data']
        actual_text = alert.text
        assert expected_text in actual_text, f"❌ 当前text: {actual_text} 不包含 预期text: {expected_text}"

    @kw_step
    def assert_element_exist(self, step):
        element = self.find(step)
        assert element, f"❌ 元素不存在: {element}"
        logging.info(f"✅ 元素存在 {element}")