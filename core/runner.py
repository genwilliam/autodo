from core.reader import get_question, get_options, get_question_type
from core.solver import solve, solve_text, solve_blank

def auto_run(page):
    while True:
        question = get_question(page)
        qtype = get_question_type(page)

        print("\n=== 题目 ===\n", question)
        print("题型：", qtype)

        if qtype in ("single", "multi"):
            options = get_options(page)
            print("\n=== 选项 ===")
            for l, t in options:
                print(f"{l}. {t}")

            answer = solve(question, options)
            print("\nAI 选择：", answer)
            click_option(page, answer, qtype)

        elif qtype == "text":
            answer = solve_text(question)
            print("\nAI 简答：", answer)
            fill_text_answer(page, answer)

        elif qtype == "blank":
            answer = solve_blank(question)
            print("\nAI 填空：", answer)
            fill_blank_answer(page, answer)

        else:
            print("无法识别题型，跳过本题")

        page.locator("button:has-text('下一题')").click()
        page.wait_for_timeout(500)


def click_option(page, answer, qtype):
    if qtype == "single":
        # 单选题
        label = page.locator(f"label.option-select:has(input[value='{answer}'])")
        try:
            label.click(force=True)
        except:
            label.locator(".el-radio__inner").click(force=True)

    elif qtype == "multi":
        # 多选题
        answers = [x.strip() for x in answer.split(",")]

        for ans in answers:
            label = page.locator(f"label.option-select:has(input[value='{ans}'])")
            try:
                label.click(force=True)
            except:
                label.locator(".el-checkbox__inner").click(force=True)




def fill_text_answer(page, answer: str):
    """
    往 CKEditor 简答题编辑框里输入文本
    """
    editor = page.locator("div.ck-editor__editable").first

    # 点击激活编辑器
    editor.click()
    page.wait_for_timeout(100)

    # 全选现有内容并删除
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")

    # 输入答案（type 最安全，会触发 onChange）
    page.keyboard.type(answer)



def fill_blank_answer(page, answer: str):
    """
    填空题自动填写（textarea 优先，contenteditable 次之）
    """
    # textarea
    textarea = page.locator("textarea.el-textarea__inner")
    if textarea.count() > 0:
        textarea.first.fill(answer)
        return

    # contenteditable div（plaintext-only）
    editable = page.locator("div[contenteditable='plaintext-only']")
    if editable.count() > 0:
        editable.first.click()
        page.keyboard.type(answer)
        return

    input_box = page.locator("input[type='text']")
    if input_box.count() > 0:
        input_box.first.fill(answer)
        return

    print("未找到填空题输入框，跳过。")