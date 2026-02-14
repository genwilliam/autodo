from playwright.sync_api import sync_playwright
from utils.config_loader import get_url

def label():
    url = get_url()

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        # 使用登录状态
        context = browser.new_context(storage_state="config/login_state.json")
        page = context.new_page()

        page.goto(url)
        print("已自动登录")

        print("按 Enter 获取 <p> 标签内容，按 q 然后回车退出程序")

        while True:
            key = input("\n等待操作（Enter = 获取；q = 退出）：")

            if key.lower() == "q":
                print("程序结束，再见！")
                break

            print("\n===== 获取到的 <p> 标签文本 =====\n")

            # 重新获取当前页面的所有 p 标签
            p_tags = page.locator("p").all()

            for tag in p_tags:
                try:
                    print(tag.inner_text())
                except:
                    print("[无法读取标签内容]")

            print("\n（你现在可以点击下一题，然后按 Enter 再次获取。）")