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
import Osbtlib, BrowserSimulator from osbtlib
```

`Osbtlib` includes a client that interacts with proxy extensions, a client that interacts with the Attacker OP, and the ability to manipulate ID Token.

`BrowserSimulator` includes the ability to automate browser operations using [PlayWright](https://playwright.dev/).

```py
osbt = Osbtlib(
    proxy_extension_url = "http://localhost:5555",
    attacker_op_url = "http://localhost:9997",
    cli_server_url = "http://localhost:54454"
)

bs = BrowserSimulator(
    url = "http://localhost:9999/login",
    proxy_url = "http://localhost:8080"
)
```

Create an instance of `Osbtlib`. The arguments are as follows:
- `proxy_extension_url` : URL of proxy extension server
- `attacker_op_url`: URL of attacker op
- `cli_server_url`: URL of osbt server

Create an instance of `BrowserSimulator`. The arguments are as follows:
- `url`: URL of login page
- `proxy_url`: URL of proxy server

### Proxy Server Operation `Osbtlib.proxy`
#### add, modify request header
```py
osbt.proxy.add_header("header_name", "header_value")
osbt.proxy.modify_header("modified_header_name", "header_value")
```

> `add_header(name: str, value: str) -> dict`
- `name`: Name of the header to be added
- `value`: Value of the header to be added

> `modify_header(name: str, value: str) -> dict`
- `name`: Name of the header to be replaced
- `value`: Value of the header to be replaced

#### add, modify request query param
```py
osbt.proxy.add_query_param("param_name", "param_value")
osbt.proxy.modify_query_param("modified_param_name", "param_value")
```
> `add_query_param(name: str, value: str) -> dict`
- `name`: Name of the query param to be added
- `value`: Value of the query param to be added

> `modify_query_param(name: str, value: str) -> dict`
- `name`: Name of the query param to be replaced
- `value`: Value of the query param to be replaced

#### add, modify request body param
```py
osbt.proxy.add_body_param("param_name", "param_value")
osbt.proxy.modify_body_param("modified_param_name", "param_value")
```
> `add_body_param(name: str, value: str) -> dict`
- `name`: Name of the body param to be added
- `value`: Value of the body param to be added

> `modify_body_param(name: str, value: str) -> dict`
- `name`: Name of the body param to be replaced
- `value`: Value of the body param to be replaced

#### intercept request/response
```py
osbt.proxy.intercept_request("condition")
osbt.proxy.intercept_response("condition")
```
> `intercept_request(condition: str) -> dict`
- `condition`: Requests containing this string are dropped

> `intercept_response(condition: str) -> dict`
- `condition`: Responses containing this string are dropped

#### get request/response history
```py
osbt.proxy.get_history()
```
> `get_history() -> dict`

#### delete all rules and history
```py
osbt.proxy.clean()
```
> `clean() -> dict`

### Attacker OP Operation `Osbtlib.attacker-op`
#### ID Token Replacement for Responses

#### Providing malicious endpoints using the Discovery service

#### Redirect to Honest OP upon an authentication request

### Browser Simulator Operation `BrowserSimulator`

### CLI Operation `Osbtlib.cli`

#### send test result to osbt server
```py
osbt.cli.send_result(
    "IDSpoofing",
    "- The attacker op modifies the id_token to impersonate the victim <br> - The sub claim of the id_token is modified to the victim's sub claim",
    "Passed",
    "",
    "- Check the signature of the id_token <br> - Check the iss claim of the id_token <br> - Check the sub claim of the id_token"
)
```
> `send_result(test_name: str, description: str, outcome: str, err_msg: str, countermeasure: str) -> dict`

### Others
#### ID Token Operation `Osbtlib.id_token`

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
