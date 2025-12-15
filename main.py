import time
from time import sleep

from playwright.sync_api import sync_playwright
from utils.config_loader import get_url
from core.runner import auto_run

def main():
    url = get_url()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        # browser = p.webkit.launch(headless=False)
        context = browser.new_context(storage_state="config/login_state.json")
        page = context.new_page()
        page.goto(url)

        print("已自动登录，开始自动刷题！")
        # sleep 6s
        time.sleep(6)
        auto_run(page)

if __name__ == "__main__":
    main()