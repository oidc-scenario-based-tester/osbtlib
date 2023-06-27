from src import proxy
from src import browser

if __name__ == "__main__":
    # client = proxy.ProxyClient("localhost", 5555)
    # client.add_header("HOGE-HUGA", "hogehoge")
    # client.modify_header("HOGE-HUGA", "hugahuga")
    # client.add_body_param("hoge", "piyo")
    # client.modify_body_param("username", "yuasa2")
    # client.intercept("huga")

    bs = browser.BrowserSimulator("https://example.com")
    bs.run('''page.goto("https://playwright.dev/")
page.screenshot(path="example.png")
    ''')