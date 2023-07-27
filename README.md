# osbtlib
Scenario description library for [oidc-scenario-based-tester/osbt](https://github.com/oidc-scenario-based-tester/osbt)

## Install

```
pip install osbtlib
```

## Setup
Installation of `Python`, `pip` and [oidc-scenario-based-tester/osbt](https://github.com/oidc-scenario-based-tester/osbt) is required.

## Quick Start
Write a test scenario script.

```
$ touch scenario.py
```

```py
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
    redirect_uri = 'https://example.com'
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
```

Run example RP and OP in [zitadel/oidc](https://github.com/zitadel/oidc).

```
# start oidc op server
$ go run github.com/zitadel/oidc/v2/example/server

# start oidc web client (in a new terminal)
$ CLIENT_ID=web CLIENT_SECRET=secret ISSUER=http://localhost:9998/ SCOPES="openid profile" PORT=9999 go run github.com/zitadel/oidc/v2/example/client/app
```

Run osbt server and proxy server extension.

```
$ osbt server
$ mitmdump -s proxy.py
```

Then execute scenario script by `osbt run`.

```
$ osbt run -f scenario.py -t 30
```

## Usage
### Import

```py
import osbtlib
```

### Proxy Server Operation

### Attacker OP Operation

### Browser Simulator Operation

### Others
#### ID Token Operation

## Test
```
// Run all tests
$ python -m pytest

// Run only test that do not use the server and proxy
$ python -m pytest -m "not server and not proxy"

// Run only tests that do not use the server
$ python -m pytest -m "not server"

// Run only tests that use the server
$ python -m pytest -m "server"
```
