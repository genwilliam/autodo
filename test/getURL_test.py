import yaml
import os

# 获取当前脚本 getURL_test.py 所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 得到 config.yaml 的真实路径
config_path = os.path.join(BASE_DIR, "../config/config.yaml")

# 规范化路径（将 ../ 处理成绝对路径）
config_path = os.path.normpath(config_path)

with open(config_path, "r") as f:
    cfg = yaml.safe_load(f)

print(cfg["url"])