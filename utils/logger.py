# utils/logger.py
# utils/logger.py
import logging

# 统一用一个项目级的名字，别用 __name__
logger = logging.getLogger("webatf")

# 关键：显式把这个logger的级别设成INFO
logger.setLevel(logging.INFO)

# 不在这里加 handler，交给 pytest.ini 去加
# 否则你run.py单独跑的时候想加也可以在这里加
