import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../osbtlib'))

from osbtlib import BrowserSimulator

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

bs = BrowserSimulator('http://localhost:9999/login', 'http://localhost:8080')
bs.run(sso_flow)
bs.close()