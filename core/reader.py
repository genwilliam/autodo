from playwright.sync_api import Page


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
        通用选项提取（适用于单选/多选)
        每个选项都是 label.option-select
        input 类型:
            多选 = input.el-checkbox__original
            单选 = input.el-radio__original
    """
    options = []

    labels = page.locator("label.option-select")

    for i in range(labels.count()):
        label_obj = labels.nth(i)

        # A/B/C/D 获取 input 的 value="A"
        input_el = label_obj.locator("input")
        option_letter = input_el.get_attribute("value").strip()

        # 选项文本  在 div.qst-html p 中
        option_text = label_obj.locator("div.qst-html p").inner_text().strip()

        options.append((option_letter, option_text))

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