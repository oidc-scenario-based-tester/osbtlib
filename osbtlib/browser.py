import sys
import re
from playwright.sync_api import sync_playwright
from .exceptions import ExecutionError, NoPageAvailableError, NoContentAvailableError

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
            raise ExecutionError(f"Execution Error: {str(e)}")

        # save browser and page
        self.playwright = playwright
        self.browser = browser
        self.page = page

    def visit(self, url: str):
        if self.page is not None:
            self.page.goto(url)
        else:
            raise NoPageAvailableError("Error: No page available")

    def get_content(self) -> str:
        # Get the page's HTML content
        if self.page is not None:
            page_content = self.page.content()
            return page_content
        else:
            raise NoContentAvailableError("Error: No content available")

    def close(self):
        print("Finished browser process.")
        self.page.close()
        self.browser.close()
        self.playwright.stop()