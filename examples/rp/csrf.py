import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../osbtlib'))

from osbtlib import BrowserSimulator, Osbtlib

# Test Information
test_name = "CSRF"
test_description = "csrf description"
outcome = "Failed"
err_msg = ""
countermeasure = "csrf countermeasure"

HONEST_RP_ENDPOINT = "http://localhost:9999"
PROXY_SERVER_ENDPOINT = "http://localhost:8080"
PROXY_EXTENSION_ENDPOINT = "http://localhost:5555"

osbt = Osbtlib(
    proxy_extension_url = PROXY_EXTENSION_ENDPOINT
)

# victim credentials
victim_username = 'test-user@localhost'
victim_password = 'verysecure'

# attacker credentials
attacker_username = 'test-user2'
attacker_password = 'verysecure'

try:
    # add intercept rule
    osbt.proxy.intercept_response(f"{HONEST_RP_ENDPOINT}/auth/callback?code=")
    
    # login with victim account
    sso_flow = f"""
page.locator('input[name="username"]').fill('{victim_username}')
page.locator('input[name="password"]').fill('{victim_password}')
page.locator('button[type="submit"]').click()
print(page.content())
    """
    bs1 = BrowserSimulator(f'{HONEST_RP_ENDPOINT}/login', PROXY_SERVER_ENDPOINT)
    bs1.run(sso_flow)
    bs1.close()

    # replace location header
    traces = osbt.proxy.get_history()
    print("=====================================")
    for res in traces['response']:
        for name, value in res['headers'].items():
            if name == 'Location':
                location = value
    
    osbt.proxy.clean()

    # login with attacker account
    sso_flow = f"""
page.locator('input[name="username"]').fill('{attacker_username}')
page.locator('input[name="password"]').fill('{attacker_password}')
page.locator('button[type="submit"]').click()
print(page.content())
    """
    bs2 = BrowserSimulator(f'{HONEST_RP_ENDPOINT}/login', PROXY_SERVER_ENDPOINT)
    bs2.run(sso_flow)

    # visit location
    print("location:", location)
    bs2.visit(location)
    content = bs2.get_content()
    print("content:", content)
    bs2.close()

    # result check
    if "failed to get state" in content:
        outcome = "Passed"
    
    osbt.cli.send_result(test_name, test_description, outcome, err_msg, countermeasure)

except Exception as e:
    print('Error:', e)
    osbt.proxy.clean()

    outcome = "Failed"
    err_msg = str(e)
    osbt.cli.send_result(test_name, test_description, outcome, err_msg, countermeasure)