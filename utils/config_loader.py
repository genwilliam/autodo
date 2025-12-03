import yaml
import os

def load_config():
    # 获取当前文件所在目录（utils）
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 找到 config.yaml 的路径
    config_path = os.path.join(base_dir, "../config/config.yaml")
    config_path = os.path.normpath(config_path)

    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_url():
    cfg = load_config()
    return cfg["url"]