import sys
import re
from playwright.sync_api import sync_playwright

class BrowserSimulator:
    def __init__(self, url: str, proxy_url: str):
        self.url = url
        self.proxy_url = proxy_url
        self.browser = None
        self.page = None

    def run(self, script: str):
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(proxy={"server": self.proxy_url})
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.goto(self.url)

        # Execute login flow
        try:
            exec(script)
        except Exception as e:
            print("Execution Error:", e)
            sys.exit()

        # save browser and page
        self.browser = browser
        self.page = page

    def search_on_page(self, target: str) -> bool:
        # Get the page's HTML content
        page_content = self.page.content()
        # Check if the target string is in the page content
        return target in page_content

    def close(self):
        print("Finished browser process.")
        self.browser.close()


