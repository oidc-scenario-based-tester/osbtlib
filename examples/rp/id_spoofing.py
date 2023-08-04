import sys
import os
import time
import jwt

sys.path.append(os.path.join(os.path.dirname(__file__), '../../osbtlib'))

from osbtlib import BrowserSimulator, Osbtlib

# Test Information
test_name = "IDSpoofing"
test_description = "- The attacker op modifies the id_token to impersonate the victim <br> - The sub claim of the id_token is modified to the victim's sub claim"
outcome = "failed"
err_msg = ""
countermeasure = "- Check the signature of the id_token <br> - Check the iss claim of the id_token <br> - Check the sub claim of the id_token"


ATTACKER_OP_ENDPOINT = "http://localhost:9997"
HONEST_RP_ENDPOINT = "http://localhost:9999"
PROXY_SERVER_ENDPOINT = "http://localhost:8080"

osbt = Osbtlib(
    attacker_op_url = ATTACKER_OP_ENDPOINT
)

bs = BrowserSimulator(f'{HONEST_RP_ENDPOINT}/login?issuer={ATTACKER_OP_ENDPOINT}/', PROXY_SERVER_ENDPOINT)

try:
    # create malicious id_token
    malicious_id_token = jwt.encode({"issuer": "http://localhost:9997/", "sub": "hoge"}, key="", algorithm="none")

    # send order to attacker op
    res = osbt.attacker_op.replace_id_token(malicious_id_token)
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
    
    bs.run(sso_flow)
    content = bs.get_content()
    print("content:", content)
    bs.close()

    # result check
    if "issuer does not match" in content:
        outcome = "pass"

    osbt.attacker_op.clean()

    osbt.cli.send_result(test_name, test_description, outcome, err_msg, countermeasure)
except Exception as e:
    print('Error:', e)
    osbt.attacker_op.clean()

    outcome = "failed"
    err_msg = str(e)
    osbt.cli.send_result(test_name, test_description, outcome, err_msg, countermeasure)
