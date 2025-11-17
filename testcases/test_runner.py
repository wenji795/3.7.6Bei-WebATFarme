import logging
import sys
import os
from jinja2 import Template

from core.assert_keyworks import AssertKeywords
from core.keywords import Keywords
from utils.allure_utils import allure_init
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pytest
from utils.excel_utils import read_excel

class TestRunner:


    #读取测试用例文件中的全部数据，用属性保存
    data = read_excel()

    #不确定后续是否需要提取
    # all = {}

    @pytest.mark.parametrize("case", data)#“让这个测试函数（test_case）重复执行多次，每次传入 data 里的一个元素，命名为 case。”
    def test_case(self, case, driver_handler):#driver_handler是pytest的fixture参数,从conftest.py来的

            # 引用全局的all
            # all = self.all
            #根据all的值，渲染case
            # case = eval(Template(str(case)).render(all))


            #初始化allure报告
            allure_init(case=case)#形参=实参  参数只有一个时形参可以不写
            # allure.dynamic.feature(case["feature"])
            # allure.dynamic.story(case["story"])
            # allure.dynamic.title(f"ID:{case["id"]} -- {case["title"]}")
            # logging.info(f'用例ID：{case["id"]} 模块：{case["feature"]} 场景：{case["story"]} 标题：{case["title"]}')

            #创建关键字对象
            keywords = Keywords(driver_handler)#把浏览器对象传进 Keywords 类了。关键字函数都能通过 self.driver 去控制浏览器；
            assert_keywords = AssertKeywords(driver_handler)

            #执行每一步
            for step in case["steps"]:
                logging.info(
                    f"正在执行步骤: {step['step_num']} - 关键字: {step['keyword']} - 名称: {step['step_name']}")
                #循环遍历查找关键字
                for i in [keywords, assert_keywords]:
                    #用hasattr判断关键字是否存在
                    if hasattr(i, step['keyword']):
                        # 匹配关键字，__getattritubute__(属性名或方法名) -> 返回一个绑定方法 对象类型的数据
                        # 你不能写死keywords.input(step)，所以你要“根据字符串去拿对象的方法”__getattribute__()。
                        # 结果是拿到了一个“可以调用的函数”function_name
                        function_name = i.__getattribute__(
                            step["keyword"])  # step["keyword"] 取出来就是字符串，比如 "input"。
                        # print(function_name)
                        # 执行ta
                        function_name(step)
                        break#break是找到了关键字，即跳出循环
                else:#没找到关键字，报异常
                    raise AttributeError(f"❌没找到关键字 {step['keyword']}")





