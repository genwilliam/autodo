# Autodo —— u+ 自动化刷题助手

Autodo 是一个基于 **Playwright + Python + DeepSeek AI** 的自动刷题工具。

> 由于用的html标签识别题目,局限性很高,所以不能确保别的平台能用. 

主要功能：

- 自动加载题目  
- 自动识别题干与选项  
- 自动调用 DeepSeek AI 进行做题  
- 自动点击正确选项并进入下一题  
- 支持选择题(包括单选多选)、填空题、简答题  
- 自动保存登录状态，下次打开无需登录  



# example:

[▶️ 点击查看视频](https://github.com/genwilliam/autodo/releases/download/v1.2.3/example.mp4)

![示例](assets/examp.gif)


---

## 📦 功能特点

- 🧠 使用 DeepSeek AI 自动答题  
- 🤖 使用 Playwright 自动化网页交互  
- 🔐 登录状态自动保存，不用重复登录  

---

## **📁 项目结构说明**



```
autodo/
│
├── config/
│   ├── config.yaml              # 项目配置（如 URL）
│   └── login_state.json         # 登录状态（自动生成）
│
├── utils/
│   ├── config_loader.py         # 加载 YAML
│   └── ai_client.py             # DeepSeek AI 调用封装
│
├── auth/
│   └── save_state.py            # 首次登录保存 cookie
│
├── core/
│   ├── reader.py                # 获取题目、选项
│   ├── solver.py                # AI 解析题目
│   └── runner.py                # 自动下一题逻辑
│
├── task/
│   └── label_task.py            # 调试用：打印页面标签
│
└── main.py                      # 主入口：真正的自动刷题程序
```
---

## 🚀 使用方法


### 1. 克隆项目

```bash
git clone <https://github.com/genwilliam/autodo.git>
cd autodo
```


### **2. 创建虚拟环境(你也可以手动创建)**

```
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```
.venv\Scripts\activate
```


### **3. 安装 Python 依赖**

```
pip install -r requirements.txt
```

### **4. 安装 Playwright 浏览器内核（必须）**

```
playwright install
```

Playwright 依赖浏览器内核，否则无法打开浏览器窗口

### **5. 配置 DeepSeek API Key（必需）**

> 如果你需要把key放到环境变量中,下面的教程或许可以帮助你,这也是官方推荐的方式
> 本项目是把key放到配置文件`config/config.yaml`中,如果放到环境变量中,你可能需要修改代码
> 你可以在[这里](https://platform.deepseek.com/api_keys)获取DeepSeek API key,以及在[这里](https://api-docs.deepseek.com/zh-cn/)查看怎么调用ai
> 当然,或许你需要先[充值](https://platform.deepseek.com/top_up),实测 0.03块钱左右就可以写完50多题 + 我测试的用量

![PixPin_2025-12-03_17-15-17](https://raw.githubusercontent.com/genwilliam/picgo_img/main/img/PixPin_2025-12-03_17-15-17.png)

##### 1) 在终端中设置：

```
export DEEPSEEK_API_KEY="你的 deepseek key"
```

Mac 可写入 ~/.zshrc：

```
echo 'export DEEPSEEK_API_KEY="你的 deepseek key"' >> ~/.zshrc
source ~/.zshrc
```

Windows:

```
setx DEEPSEEK_API_KEY "你的 key"
```



##### 2) 将key写入到config.yaml中

![PixPin_2025-12-03_17-17-13](https://raw.githubusercontent.com/genwilliam/picgo_img/main/img/PixPin_2025-12-03_17-17-13.png)

> 其中:
> 第一行代表的是 u+ 的地址,你需要登录u+进入答题界面再复制粘贴过来(每次复制URL似乎比一题一题写(搜)  好点吧 )
>
> 第二行是你的API key,你需要创建一个API key(这里就不赘述了)

### **6. 首次运行：保存登录状态**


```
python auth/save_state.py
```

流程：

1. 自动打开浏览器
2. 手动完成网站登录（登录你的 eduplus 网址）
3. 回到终端按 Enter
4. 登录状态将保存到：config/login_state.json


以后无需再次登录。


### **7. 正常自动刷题运行**



```
python main.py
```

功能包括：



- 自动登录
- 自动解析题目与选项
- 调用 AI 得出答案
- 自动点击选项
- 自动点击下一题
- 按 `q + 回车` 手动退出
---
## **🛡️ 常见问题**

### **Q: 登录状态失效怎么办？**

删除旧文件：

```
rm config/login_state.json
python auth/save_state.py
```

重新登录即可。

## 📜 许可证（License）

本项目采用 **MIT License** 开源协议。

## **❤️ 作者**

如果你喜欢这个项目，可以点个 ⭐

如果需要扩展功能（记录错题、读取题库、多账号自动刷题），欢迎联系我继续完善。

## 📢 免责声明

本项目仅供 **学习、研究与个人实验** 使用。

请注意：

- 本项目的自动化功能仅用于技术学习与研究自动化测试、网页解析、AI 调用等相关知识。
- 请勿将本项目用于任何违反法律法规、侵犯平台权益、破坏系统、规避考试、刷分刷题、商业化运营等用途。
- 使用者须自行承担使用本项目产生的所有风险与后果。
- 作者不对因滥用本项目而导致的账号异常、封禁、数据丢失、法律风险等任何损失负责。
- 若你使用本项目访问的网站或服务有《用户协议》或《使用条款》，请务必遵守对应条款，不要将本项目用于任何违规行为。

如果你不同意以上协议，请立即停止使用本项目。
