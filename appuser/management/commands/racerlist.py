from django.core.management.base import BaseCommand

from raceapi.views import get_standings_request, get_drivers


class Command(BaseCommand):

    def handle(self, *args, **options):
        get_drivers()
        get_standings_request()
