import unittest
import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../osbtlib'))

from attacker_op import AttackerOPClient

class TestAttackerOPClient(unittest.TestCase):

    def setUp(self):
        self.client = AttackerOPClient("http://localhost:9997")

    @pytest.mark.server
    def test_add_task(self):
        name = 'IDSpoofing'
        args = {
            'id_token': 'foo'
        }
        task_id = self.client.add_task(name, args)
        task = self.client.get_task(task_id)
        print(task)

        self.assertEqual(name, task.get('Name'))
        self.assertDictEqual(args, task.get('Args'))