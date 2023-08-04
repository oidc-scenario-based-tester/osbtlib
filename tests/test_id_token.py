import unittest
import jwt
import json
import base64
import sys
import os

import osbtlib.id_token as id_token

class TestUtils(unittest.TestCase):
    def test_get_header(self):
        # create id_token
        original_header = {'alg': 'HS256', 'typ': 'JWT'}
        secret = 'secret'
        original_token = jwt.encode({'foo': 'bar'}, secret, algorithm='HS256', headers=original_header)

        header = id_token.get_header(original_token)
        self.assertDictEqual(header, original_header)

    def test_replace_header(self):
        # create id_token
        original_header = {'alg': 'HS256', 'typ': 'JWT'}
        secret = 'secret'
        original_token = jwt.encode({'foo': 'bar'}, secret, algorithm='HS256', headers=original_header)

        # replace original header with new header
        new_header = {'alg': 'HS256', 'typ': 'JWS'}
        new_token = id_token.replace_header(original_token, new_header)

        # decode header part
        header_decoded = id_token.get_header(new_token)

        self.assertDictEqual(header_decoded, new_header)

    def test_get_payload(self):
        # create id_token
        original_payload = {'foo': 'bar'}
        secret = 'secret'
        original_token = jwt.encode(original_payload, secret, algorithm='HS256')

        payload = id_token.get_payload(original_token)
        self.assertEqual(payload.get('foo'), 'bar')

    def test_replace_payload(self):
        # create id_token
        original_payload = {'foo': 'bar'}
        secret = 'secret'
        original_token = jwt.encode(original_payload, secret, algorithm='HS256')
        
        # replace original payload with new payload
        new_payload = {'baz': 'qux'}
        new_token = id_token.replace_payload(original_token, new_payload)
        
        # decode payload part
        payload_decoded = id_token.get_payload(new_token)
        
        self.assertDictEqual(payload_decoded, {'baz': 'qux'})

    def test_get_signature(self):
        # create id_token
        secret = 'secret'
        original_token = jwt.encode({'foo': 'bar'}, secret, algorithm='HS256')

        signature = id_token.get_signature(original_token)
        self.assertEqual(signature, original_token.split('.')[2])

    def test_replace_signature(self):
        # create id_token
        secret = 'secret'
        original_token = jwt.encode({'foo': 'bar'}, secret, algorithm='HS256')

        # replace original signature with new signature
        new_signature = 'new_signature'
        new_token = id_token.replace_signature(original_token, new_signature)
        
        signature = id_token.get_signature(new_token)
        
        self.assertEqual(signature, new_signature)
