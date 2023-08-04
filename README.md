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
import jwt

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
```

Run example RP and attacker OP.

```
# start oidc op server
$ attacker-op

# start oidc web client (in a new terminal)
$ git clone https://github.com/oidc-scenario-based-tester/osbt.git
$ cd osbt
$ CLIENT_ID=web CLIENT_SECRET=secret ISSUER=http://localhost:9997/ SCOPES="openid profile" PORT=9999 go run github.com/oidc-scenario-based-tester/osbt/oidc/rp/user-selected
```

Run osbt server and proxy server extension.

```
$ osbt server
$ mitmdump -s proxy-extension.py
```

Then execute scenario script by `osbt run`.

```
$ osbt run -f scenario.py -t 30s
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
```py
osbt.attacker_op.replace_id_token("[id_token]")
```
> `replace_id_token(id_token: str) -> bool`
- `id_token`: The value after replacement of the ID token in the response from the Attacker OP.

#### Providing malicious endpoints using the Discovery service
```py
osbt.attacker_op.set_malicious_endpoints({
    "authorization_endpoint": "http://localhost:9999/auth"
})
```
> `set_malicious_endpoints(endpoints: dict) -> bool`
- `endpoints`: Change the endpoints that Attacker OP returns when `/.well-known/openid-configuration` is accessed. The following endpoints can be changed.
  - `authorization_endpoint`
  - `token_endpoint`
  - `userinfo_endpoint`
  - `registration_endpoint`

#### Redirect to Honest OP upon an authentication request
```py
osbt.attacker_op.idp_confusion("http://localhost:9998/auth")
```
> `idp_confusion(honest_op_auth_endpoint: str) -> bool`
- `honest_op_auth_endpoint`: `authorization_endpoint` of the honest OP. When an authentication request is sent to the Attacker OP, it is redirected to this endpoint with the query parameters passed on.

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
##### get, replace header
```py
osbt.id_token.get_header("[id_token]") # {'alg': 'HS256', 'typ': 'JWT'}
osbt.id_token.replace_header("[id_token]", {'alg': 'HS256', 'typ': 'JWS'}) 
```
> `get_header(id_token: str) -> dict`
- `id_token`: ID token for which the header will be obtained.
> `replace_header(id_token: str, new_header: dict) -> str`
- `id_token`: ID token for which the header will be replaced.
- `new_header`: Header of ID token after replacement.

##### get, replace payload
```py
osbt.id_token.get_payload("[id_token]") # {'sub': '1234', 'username': 'guest'}
osbt.id_token.replace_payload("[id_token]", {'sub': '1234', 'username': 'guest'}) 
```
> `get_payload(id_token: str) -> dict`
- `id_token`: ID token for which the payload will be obtained.
> `replace_payload(id_token: str, new_payload: dict) -> str`
- `id_token`: ID token for which the payload will be replaced.
- `new_payload`: Payload of ID token after replacement.
  
##### get, replace signature
```py
osbt.id_token.get_signature("[id_token]") # SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
osbt.id_token.replace_header("[id_token]", "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c") 
```
> `get_signature(id_token: str) -> str`
- `id_token`: ID token for which the signature will be obtained.
> `replace_header(id_token: str, new_signature: str) -> str`
- `id_token`: ID token for which the signature will be replaced.
- `new_signature`: Header of ID token after replacement.

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
