from django.core.management.base import BaseCommand
from raceapi.views import get_standings_request, race_results, tally


class Command(BaseCommand):

    def handle(self, *args, **options):
        get_standings_request()
        race_results()
        tally()
