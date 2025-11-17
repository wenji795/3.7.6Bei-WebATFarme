#driver_utils.py
#根据config.py中的浏览器配置项，创建哪种浏览器对象 使用哪种驱动模式 是否开启无头模式
from config.config import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.logger import logger

def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # 是否无头模式
    if HEADLESS:
        options.add_argument("--headless")

    # 本地模式 & 远程模式分支
    if DRIVER_TYPE == "local":
        # ✅ 改这里：不再用固定路径，让 Selenium 或 webdriver_manager 自己安装正确版本
        # 方式1：使用 Selenium Manager（推荐，最简洁）
        # driver = webdriver.Chrome(options=options)

        # 方式2：使用 webdriver_manager（推荐用于稳定 CI 环境）
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(options=options, service=service)
    else:
        # 远程执行（例如 Selenium Grid 或 Docker）
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(options=options, service=service)

    logger.info("✅ 启动 Chrome 浏览器成功")
    return driver

def get_edge_driver():
    pass