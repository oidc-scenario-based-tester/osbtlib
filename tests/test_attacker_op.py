import unittest
import pytest
import sys
import os

from osbtlib.attacker_op import AttackerOPClient

class TestAttackerOPClient(unittest.TestCase):

    def setUp(self):
        self.client = AttackerOPClient("http://localhost:9997")

    @pytest.mark.server
    def test_replace_id_token(self):
        new_id_token = 'foo'
        result = self.client.replace_id_token(new_id_token)
        self.assertTrue(result)

    @pytest.mark.server
    def test_set_malicious_endpoints(self):
        endpoints = {'endpoint1': 'http://malicious.com', 'endpoint2': 'http://evil.com'}
        result = self.client.set_malicious_endpoints(endpoints)
        self.assertTrue(result)

    @pytest.mark.server
    def test_idp_confusion(self):
        honest_op_auth_endpoint = 'http://honest.com/auth'
        result = self.client.idp_confusion(honest_op_auth_endpoint)
        self.assertTrue(result)
    
    @pytest.mark.server
    def test_clean(self):
        result = self.client.clean()
        self.assertTrue(result)