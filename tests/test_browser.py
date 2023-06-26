import unittest
import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from browser import BrowserSimulator

class TestBrowserSimulator(unittest.TestCase):

    @pytest.mark.burp
    def setUp(self):
        self.simulator = BrowserSimulator('https://example.com', 'http://localhost:8080')
        self.simulator.run("""
print(page.url)
        """)
    
    @pytest.mark.burp
    def tearDown(self):
        self.simulator.close()
    
    @pytest.mark.burp
    def test_search_on_page(self):
        # Ensure a known text is found
        self.assertTrue(self.simulator.search_on_page('Example Domain'))

        # Ensure a non-existent text is not found
        self.assertFalse(self.simulator.search_on_page('NonExistentText'))

if __name__ == '__main__':
    unittest.main()
