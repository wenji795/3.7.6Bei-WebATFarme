以下是 **pytest 核心机制总览图与说明**，展示执行顺序、fixture 生命周期、参数化展开、hook 流程与报告生成路径：

---

## 🧠 Pytest 执行全流程概览

```
┌────────────────────────────────────────────────────────────┐
│ pytest 启动                                               │
└──────────────┬─────────────────────────────────────────────┘
               │
               ▼
     1️⃣ 收集测试文件（test_*.py / *_test.py）
               │
               ▼
     2️⃣ 执行 conftest.py
         ├─ 注册 fixture
         ├─ 注册 hook
         └─ 加载 pytest.ini 配置
               │
               ▼
     3️⃣ 参数化展开
         ├─ 识别 @pytest.mark.parametrize()
         └─ 为每组数据创建独立的 test 实例
               │
               ▼
     4️⃣ Fixture 生命周期管理
         ├─ function: 每个测试独立实例（默认）
         ├─ class: 整个类共享
         ├─ module: 每个文件共享
         └─ session: 整个运行周期共享
               │
               ▼
     5️⃣ 执行测试（含 hook 调用）
         ├─ pytest_runtest_setup(item)
         ├─ 调用 fixture (yield 前)
         ├─ 运行测试函数
         ├─ 调用 fixture (yield 后)
         └─ pytest_runtest_teardown(item)
               │
               ▼
     6️⃣ 测试报告与插件交互
         ├─ allure / pytest-html 收集日志、截图、参数
         ├─ pytest_runtest_logreport 生成结果节点
         └─ pytest_sessionfinish 输出最终报告
               │
               ▼
┌────────────────────────────────────────────────────────────┐
│ ✅ 测试结束，生成报告（HTML / Allure / JUnit 等）          │
└────────────────────────────────────────────────────────────┘
```

---

## ⚙️ fixture 生命周期可视化

```
@pytest.fixture(scope="function")
        │
        ├─ setup 阶段 (yield 前) → 启动浏览器 / 创建连接
        │
        ├─ 测试函数执行 (使用 fixture 返回对象)
        │
        └─ teardown 阶段 (yield 后) → 关闭浏览器 / 清理资源
```

| scope | 启动时机 | 销毁时机 | 典型用途 |
|--------|-----------|-----------|-----------|
| function | 每个测试 | 每个测试后 | 浏览器、文件句柄 |
| class | 每个类 | 类结束 | 同类测试共享资源 |
| module | 每个文件 | 文件结束 | 模块级环境 |
| session | 整个运行 | 运行结束 | 全局配置、登录 |

---

## 🧩 参数化展开机制

```
@pytest.mark.parametrize("case", data)
     │
     └─> data = [case_1, case_2, case_3]
             │
             ├─ test_case(case_1)
             ├─ test_case(case_2)
             └─ test_case(case_3)
```

📦 每个 `case` 是从 Excel 读取的测试用例字典：
```python
{
  "id": "test_1",
  "title": "注册页面",
  "steps": [ {"keyword": "open", "data": "url"}, ... ]
}
```
pytest 自动为每个 case 生成独立的测试实例。  
执行时 fixture (`driver_handler`) 自动注入，形成完整闭环。

---

## 🔗 Hook 执行顺序（核心生命周期）

| Hook 名称 | 作用 |
|------------|------|
| `pytest_sessionstart()` | 测试会话开始前执行 |
| `pytest_collection_modifyitems()` | 收集完用例后可修改执行顺序 |
| `pytest_runtest_setup(item)` | 每个测试执行前 |
| `pytest_runtest_call(item)` | 实际调用测试函数 |
| `pytest_runtest_teardown(item)` | 每个测试后清理 |
| `pytest_sessionfinish(session)` | 整个 session 结束后执行 |

---

## 🧱 报告生成路径 (以 Allure 为例)

```
pytest 执行 → allure.step() 捕获日志 → allure-results/
     │
     └─> allure generate allure-results -o allure-report
             │
             └─> HTML 可视化测试报告
```

Allure 将 fixture、parametrize、步骤日志整合为：
```
Feature → Story → Title → Step → Attachments
```
支持截图、输入数据、异常堆栈等可视化呈现。

---

## ✅ 总结：pytest 核心机制全景

| 机制 | 关键功能 | 用途 |
|------|-----------|------|
| fixture | 资源管理 | 启动/关闭浏览器、数据库等 |
| parametrize | 数据驱动 | Excel、JSON、API 测试 |
| marker | 测试标签 | 控制执行集 |
| hook | 插入逻辑 | 日志、截图、报告 |
| conftest.py | 共享配置 | 全局 fixture / hook |
| 命令行参数 | 动态配置 | 环境控制、浏览器选择 |
| 插件系统 | 扩展能力 | 报告、重跑、并行 |
| allure 报告 | 可视化 | 丰富的测试追踪 |

---

📘 **一句话总结**：
> pytest = fixture 资源管理 + parametrize 数据驱动 + hook 流程控制 + 插件报告生态
> 是一套高度自动化、可扩展、可视化的测试执行框架。

