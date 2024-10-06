    """
        Django command to wait for DB to be available
    """
    
from django.core.management import BaseCommand

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        pass