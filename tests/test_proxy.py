import unittest
import pytest
import sys
import os

from osbtlib.proxy import ProxyClient

class TestProxyClient(unittest.TestCase):

    @pytest.mark.proxy
    def setUp(self):
        self.client = ProxyClient("http://localhost:5555")
    
    @pytest.mark.proxy
    def test_add_header(self):
        res = self.client.add_header("hoge", "hoge", "host", "path", "method")
        self.assertEqual("ok", res["status"])
        

    @pytest.mark.proxy
    def test_modify_header(self):
        res = self.client.modify_header("hoge", "huga", "host", "path", "method")
        self.assertEqual("ok", res["status"])

    @pytest.mark.proxy
    def test_add_query_param(self):
        res = self.client.add_query_param("hoge", "hoge", "host", "path", "method")
        self.assertEqual("ok", res["status"])

    @pytest.mark.proxy
    def test_modify_query_param(self):
        res = self.client.modify_query_param("hoge", "huga", "host", "path", "method")
        self.assertEqual("ok", res["status"])

    @pytest.mark.proxy
    def test_add_body_param(self):
        res = self.client.add_body_param("hoge", "huga", "host", "path", "method")
        self.assertEqual("ok", res["status"])

    @pytest.mark.proxy
    def test_modify_body_param(self):
        res = self.client.modify_body_param("hoge", "piyo", "host", "path", "method")
        self.assertEqual("ok", res["status"])

    @pytest.mark.proxy
    def test_intercept_request(self):
        res = self.client.intercept_request("host", "path", "method")
        self.assertEqual("ok", res["status"])
    
    @pytest.mark.proxy
    def test_intercept_response(self):
        res = self.client.intercept_response("host", "path", "method")
        self.assertEqual("ok", res["status"])
    
    @pytest.mark.proxy
    def test_get_history(self):
        res = self.client.get_history()
        self.assertEqual("ok", res["status"])
        
    @pytest.mark.proxy
    def test_clean(self):
        res = self.client.clean()
        self.assertEqual("ok", res["status"])

if __name__ == '__main__':
    unittest.main()
