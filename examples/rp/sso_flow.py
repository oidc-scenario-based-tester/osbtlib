import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from browser import BrowserSimulator

# browser simulation
sso_flow = """
page.locator('input[name="login"]').fill('hoge')
page.locator('input[name="password"]').fill('huga')
page.locator('button[type="submit"]').click()
page.locator('button[type="submit"]').click()
"""
simulator = BrowserSimulator('http://localhost:5000/login', 'http://localhost:8080')
simulator.run(sso_flow)
simulator.close()