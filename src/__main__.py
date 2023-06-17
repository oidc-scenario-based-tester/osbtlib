from src import burp

if __name__ == "__main__":
    client = burp.BurpClient("localhost", 5555)
    client.add_header("HOGE-HUGA", "hogehoge")
    client.modify_header("HOGE-HUGA", "hugahuga")
    client.add_body_param("hoge", "piyo")
    client.modify_body_param("username", "yuasa2")
    # client.intercept("huga")