import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../osbtlib'))

from osbtlib import BrowserSimulator, Osbtlib

# Test Information
test_name = "CovertRedirect"
test_description = "covert redirect description"
outcome = "failed"
err_msg = ""
countermeasure = "covert redirect countermeasure"

HONEST_RP_ENDPOINT = "http://localhost:9999"
HONEST_OP_ENDPOINT = "http://localhost:9998"
PROXY_SERVER_ENDPOINT = "http://localhost:8080"
PROXY_EXTENSION_ENDPOINT = "http://localhost:5555"

# victim credentials
victim_username = 'test-user@localhost'
victim_password = 'verysecure'

osbt = Osbtlib(
    proxy_extension_url = PROXY_EXTENSION_ENDPOINT
)

bs = BrowserSimulator(f'{HONEST_RP_ENDPOINT}/login?issuer={HONEST_OP_ENDPOINT}/', PROXY_SERVER_ENDPOINT)

try:
    # replace redirect_uri
    redirect_uri = 'https://eo2zoljihgn2f5z.m.pipedream.net'
    osbt.proxy.modify_query_param('redirect_uri', redirect_uri)    
    
    bs.run("")
    content = bs.get_content()
    print("content:", content)
    bs.close()

    # result check
    if "The requested redirect_uri is missing" in content:
        outcome = "pass"

    osbt.proxy.clean()

    osbt.cli.send_result(test_name, test_description, outcome, err_msg, countermeasure)
except Exception as e:
    print('Error:', e)
    osbt.proxy.clean()

    outcome = "failed"
    err_msg = str(e)
    osbt.cli.send_result(test_name, test_description, outcome, err_msg, countermeasure)
