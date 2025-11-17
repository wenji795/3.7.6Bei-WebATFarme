import allure
import logging

# 定义装饰器
def kw_step(func):
    def wrapper(self, step):
        """
        装饰器功能：
        1️⃣ 自动在 allure 报告中添加步骤信息；
        2️⃣ 自动记录 logging 日志；
        3️⃣ 自动调用被装饰的关键字方法。
        """
        step_num = step.get('step_num')
        step_name = step.get('step_name')
        by = step.get('by')
        value = step.get('value')

        with allure.step(f"第{step_num}步: {step_name}"):
            logging.info(f"第{step_num}步: {step_name} - 元素({by}, {value}) - 数据({step['data']}) - 索引({step['index']})")
            return func(self, step)  # 调用被装饰的函数

    return wrapper
