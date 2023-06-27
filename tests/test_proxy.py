import unittest
import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from proxy import ProxyClient

class TestProxyClient(unittest.TestCase):

    @pytest.mark.proxy
    def setUp(self):
        self.client = ProxyClient("localhost", 5555)
    
    @pytest.mark.proxy
    def test_add_header(self):
        self.client.add_header("HOGE", "hoge")

    @pytest.mark.proxy
    def test_modify_header(self):
        self.client.modify_header("HOGE", "huga")

    @pytest.mark.proxy
    def test_add_body_param(self):
        self.client.add_body_param("hoge", "huga")

    @pytest.mark.proxy
    def test_modify_body_param(self):
        self.client.modify_body_param("hoge", "piyo")

    @pytest.mark.proxy
    def test_intercept(self):
        self.client.intercept("aaaaa")

if __name__ == '__main__':
    unittest.main()
