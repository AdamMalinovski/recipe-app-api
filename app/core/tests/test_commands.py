
"""
Text custom commands for django

"""

from unittest.mock import patch


from psycopg2 import OperationalError as Psycopg2OperationalError

from django.core.management import call_command

from django.db.utils import OperationalError

from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandsTests(SimpleTestCase):

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db when db is available"""
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    # write test to check if db is not available
    @patch('time.sleep')
    def test_wait_for_db_not_ready(self, patched_sleep, patched_check):
        """Test waiting for db when db is not available"""
        patched_check.side_effect = [Psycopg2OperationalError] * 2 + \
            [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
