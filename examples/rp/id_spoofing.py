import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../osbtlib'))

from osbtlib import BrowserSimulator, Osbtlib

# Test Information
test_name = "IDSpoofing"
test_description = "- The attacker op modifies the id_token to impersonate the victim <br> - The sub claim of the id_token is modified to the victim's sub claim"
outcome = "Failed"
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
    original_id_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtleXN0b3JlLUNIQU5HRS1NRSJ9.eyJzdWIiOiJob2dlIiwiYXRfaGFzaCI6InBqZ3FVZ25yb0x0RldGSDFKMHBncFEiLCJhdWQiOiJjbGllbnQiLCJleHAiOjE2ODc1OTk3MDgsImlhdCI6MTY4NzU5NjEwOCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDozMDAwIn0.tzdJYBUuTs4q-pU8pCEm3mUp4DbXZfihrZbA4M_nKQryl9S3q7bvYaj8c-dFLidGiQXSKhMX8s1WE9rNolSmPosvyBYZiRjMWDEFK8NWY4MPZ882jNy64gk-ShwZC_x2fsZ3emobQjaRrtVu3YozmE9pbPvLX8U3l46zMogQqKJfvGCHIS1lmxs4iVEnlUDHn36m4_35SrzPF5a_jry_RUpmx9_CsryzdDGM6VzovmID0PZqeSoJ9MQJbkn5oEfG70XoykAATxQsmA-HHkmfo8WbqZko1xYwzFvi8ig-K6D33Tod-KMInt9wMYpPHPmv4lZchLeZSOVgTCbwp003Bw"
    malicious_id_token = osbt.id_token.replace_payload(original_id_token, {"sub": "huga"})

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
        outcome = "Passed"

    osbt.attacker_op.clean()

    osbt.cli.send_result(test_name, test_description, outcome, err_msg, countermeasure)
except Exception as e:
    print('Error:', e)
    osbt.attacker_op.clean()

    outcome = "Failed"
    err_msg = str(e)
    osbt.cli.send_result(test_name, test_description, outcome, err_msg, countermeasure)
