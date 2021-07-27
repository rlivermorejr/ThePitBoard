from authentication.views import get_drivers
from django.core.management.base import BaseCommand

from raceapi.views import get_standings_request


class Command(BaseCommand):

    def handle(self, *args, **options):
        get_drivers()
        get_standings_request()
