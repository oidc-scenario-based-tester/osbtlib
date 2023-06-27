import unittest
import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from attacker_idp import AttackerIdPClient

class TestAttackerIdPClient(unittest.TestCase):

    def setUp(self):
        self.client = AttackerIdPClient("http://localhost:3000")

    @pytest.mark.server
    def test_add_task(self):
        name = 'IDSpoofing'
        args = {
            'id_token': 'foo'
        }
        task_id = self.client.add_task(name, args)
        task = self.client.get_task(task_id)
        print(task)

        self.assertEqual(name, task.get('name'))
        self.assertDictEqual(args, task.get('args'))