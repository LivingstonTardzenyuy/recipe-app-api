# from unittest.mock import patch
# from psycopg2 import OperationalError as Psycopg2Error
# from django.core.management import call_command
# from django.db.utils import OperationalError
# from django.test import SimpleTestCase

# @patch("core.management.commands.wait_for_db.Command.check")
# class CommandTests(SimpleTestCase):
#     def test_wait_for_db_ready(self, patched_check):
#         patched_check_return_value = True
#         call_command('wait_for_db')
        
#         patched_check_assert_called_once_with(database=['default'],)



from django.core.management.base import BaseCommand
from time import sleep
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
                db_conn.cursor()
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second...")
                sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available!"))
