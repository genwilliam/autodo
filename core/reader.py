from playwright.sync_api import Page
import re

def get_question(page: Page):
    """
        获取题目文本（支持单选/多选/简答）
    """
    # 单选, 多选
    locator = page.locator("div.qst-html.font-bold p")
    if locator.count() > 0:
        return locator.first.inner_text().strip()

    locator = page.locator("div.qst-html p")
    if locator.count() > 0:
        return locator.first.inner_text().strip()

    # 简答题(似乎都是用的富文本编辑器)
    editor = page.locator("div.ck-editor__editable")
    if editor.count() > 0:
        # 简答题的题目会出现在该编辑框 前面的标签中
        # 自动寻找紧邻编辑框之前的一个 p/div
        prev = editor.locator("xpath=preceding::*[self::p or self::div][1]")
        if prev.count() > 0:
            return prev.first.inner_text().strip()

    ps = page.locator("p")
    for i in range(ps.count()):
        txt = ps.nth(i).inner_text().strip()
        if not txt.startswith(("A.", "B.", "C.", "D.")):
            return txt

    return ""


def get_options(page):
    """
        通用选项提取（适用于单选/多选）
        每个选项都是 label.option-select 或 div.flex-row
    """
    options = []

    # 多选/单选的 label 结构
    labels = page.locator("label.option-select")
    for i in range(labels.count()):
        label_obj = labels.nth(i)

        # 获取选项字母
        input_el = label_obj.locator("input")
        option_letter = input_el.get_attribute("value").strip()

        # 获取选项文本
        ck_div = label_obj.locator("div.qst-html")
        if ck_div.locator("p").count() > 0:
            option_text = ck_div.locator("p").inner_text().strip()
        else:
            option_text = ck_div.inner_text().strip()

        options.append((option_letter, option_text))

    # 另一种 div.flex-row 结构
    div_rows = page.locator("div.flex-row.align-center")
    for i in range(div_rows.count()):
        row = div_rows.nth(i)
        row_text = row.inner_text().strip()
        # 用正则匹配开头字母 + "、"
        m = re.match(r"([A-Z])、", row_text)
        if m:
            letter = m.group(1)
            # 取 ck-content 内的 <p> 或 div 文本
            ck_div = row.locator("div.qst-html")
            if ck_div.locator("p").count() > 0:
                text = ck_div.locator("p").inner_text().strip()
            else:
                text = ck_div.inner_text().strip()
            options.append((letter, text))

    return options

def get_question_type(page: Page):
    """
        自动判断题型
        single: 单选
        multi: 多选
        text:简答题
    """
    # 多选题
    if page.locator("input.el-checkbox__original").count() > 0:
        return "multi"

    # 单选题
    if page.locator("input.el-radio__original").count() > 0:
        return "single"

    # 简答题
    if page.locator("div.ck-editor__editable").count() > 0:
        return "text"

    # 填空题（支持 textarea / contenteditable / text input）
    if page.locator("textarea.el-textarea__inner").count() > 0:
        return "blank"

    if page.locator("div[contenteditable='plaintext-only']").count() > 0:
        return "blank"

    if page.locator("input[type='text']").count() > 0:
        return "blank"

    return "unknown"



# def get_p_label(page):
#     return page.locator("p").first.inner_text().strip()