import unittest
import pytest
import sys
import os

from osbtlib.browser import BrowserSimulator

class TestBrowserSimulator(unittest.TestCase):

    @pytest.mark.browser
    @pytest.mark.proxy
    def setUp(self):
        self.simulator = BrowserSimulator('https://example.com', 'http://localhost:8080')
        self.simulator.run("print(page.url)")
    
    @pytest.mark.browser
    @pytest.mark.proxy
    def tearDown(self):
        self.simulator.close()
    
    @pytest.mark.browser
    @pytest.mark.proxy
    def test_get_content(self):
        # Ensure a known text is found
        self.assertTrue('Example Domain' in self.simulator.get_content())

        # Ensure a non-existent text is not found
        self.assertFalse('NonExistentText' in self.simulator.get_content())

if __name__ == '__main__':
    unittest.main()
