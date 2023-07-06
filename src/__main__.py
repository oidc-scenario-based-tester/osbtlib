from src import proxy
from src import browser

if __name__ == "__main__":
    client = proxy.ProxyClient("http://localhost:5555")
    # client.add_header("HOGE-HUGA", "hogehoge")
    # client.modify_header("HOGE-HUGA", "hugahuga")
    # client.add_body_param("hoge", "piyo")
    # client.modify_body_param("username", "yuasa2")
    # client.intercept("huga")
    # print(len(client.get_history()["request"]), len(client.get_history()["response"]))
    # for req in client.get_history()["request"]:
    #     print(req)
    # print("=====================================")
    # for res in client.get_history()["response"]:
    #     print(res)

#     bs = browser.BrowserSimulator("https://example.com")
#     bs.run('''page.goto("https://playwright.dev/")
# page.screenshot(path="example.png")
#     ''')