from time import sleep

from playwright.sync_api import sync_playwright
import re


def parse_question_data(text_list):
    """
    逻辑处理：将破碎的中文列表组合成 题干 和 选项
    """
    # 过滤掉无用的杂质（如导航、分值、提示词）
    noise_words = {"分值", "得分", "解析", "下一题", "上一题", "分", "目", "题"}
    clean_list = [t for t in text_list if t not in noise_words and len(t) > 1]

    question = ""
    options = []

    # 简单的启发式判断
    # 在 U+ 平台中，通常前几项合并起来是题干，后面较长的项是选项
    # 我们寻找“选项”的特征（例如包含“上述说法”或者是列表的后半部分）

    if len(clean_list) > 2:
        # 假设前两项合并为题干（例如：'关于程序', '下列说法不正确的是'）
        question = "".join(clean_list[:2])
        # 剩下的作为选项
        options = clean_list[2:]

    return question, options


def demo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="../config/login_state.json")
        page = context.new_page()

        page.goto("https://www.eduplus.net/course/workAnswer/9a7735a67ff34d0082895db57146c101/5ed0f7ebc30745a7a33264e2c0591006/true?isPiYue=noPiYue")
        print("已自动登录，等待页面加载...")
        sleep(6)
        # 核心：直接获取所有可见的文本块，而不是源码
        # 'innerText' 会返回用户在屏幕上看到的干净文字
        raw_text = page.locator("body").inner_text()

        # 使用正则按行切分，或者按中文块切分
        lines = raw_text.split('\n')

        # 提取每一行中的中文
        chinese_pattern = r'[\u4e00-\u9fa5]+'
        structured_data = []
        for line in lines:
            match = re.search(chinese_pattern, line)
            if match and len(line.strip()) > 1:
                structured_data.append(line.strip())

        # 进行逻辑分类
        q, opts = parse_question_data(structured_data)

        print("-" * 30)
        print(f"【识别到的题干】：\n{q}")
        print("-" * 30)
        print("【识别到的选项】：")
        for i, opt in enumerate(opts):
            print(f"{chr(65 + i)}. {opt}")

        browser.close()


if __name__ == '__main__':
    demo()