from playwright.sync_api import sync_playwright

def save_login_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 登录
        page.goto("https://www.eduplus.net")

        print("请手动完成登录...")
        input("登录完成后按回车保存登录状态：")

        # 保存 cookie, localstorage
        context.storage_state(path="../config/login_state.json")

        print("登录状态已保存到 login_state.json")

if __name__ == "__main__":
    save_login_state()