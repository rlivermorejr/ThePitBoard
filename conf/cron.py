from raceapi.views import get_standings_request, race_results, tally


def cronfunction():
    get_standings_request()
    race_results()
    tally()
