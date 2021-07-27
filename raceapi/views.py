from notification.models import Notification, UpdateNotification
from django.shortcuts import render
from raceapi.models import DriverStandingsModel, RaceResults
import requests
from appuser.models import UserModel
from datetime import date, datetime


def get_standings_request():
    url = 'http://ergast.com/api/f1/current/driverStandings.json'
    response = requests.get(url)
    data = response.json()
    i = 0
    DriverStandingsModel.objects.all().delete()
    while i <= 19:
        drivers = (data['MRData']['StandingsTable']['StandingsLists'][0]
                   ['DriverStandings'][i])
        driver_data = DriverStandingsModel(
            id=i,
            given_name=drivers['Driver']['givenName'],
            family_name=drivers['Driver']['familyName'],
            dob=drivers['Driver']['dateOfBirth'],
            nationality=drivers['Driver']['nationality'],
            code=drivers['Driver']['code'],
            permanent_number=drivers['Driver']['permanentNumber'],
            position=drivers['position'],
            points=drivers['points'],
            wins=drivers['wins'],
            constructor_name=drivers['Constructors'][0]['constructorId'],
            cons_nat=drivers['Constructors'][0]['nationality'],
            full_name=drivers['Driver']['givenName'] + " " +
            drivers['Driver']['familyName']
        )
        driver_data.save()
        i += 1


def get_standings(request):
    count = len(
        [notified for notified in Notification.objects.filter(
            receiver__id=request.user.id)])

    all_drivers = DriverStandingsModel.objects.all()
    user = UserModel.objects.get(id=request.user.id)
    racerList = list(user.racer.all())
    racers = []
    locked = ""

    for racer in racerList:
        racers.append(racer.full_name)

    if date.today().weekday() == 6 and str(datetime.now().time()).split(" ")[0] < '03:00:00':

        locked = True

    return render(request, 'standings_detail.html',
                  {"all_drivers": all_drivers, 'racerList': racers,
                   'count': count, 'locked': locked})


def race_results():
    url = 'https://ergast.com/api/f1/current/last/results.json'
    response = requests.get(url)
    data = response.json()
    i = 0

    RaceResults.objects.all().delete()
    while i <= 4:
        drivers = data['MRData']['RaceTable']['Races'][0]['Results'][i]
        driver_data = RaceResults(
            id=i,
            full_name=(drivers['Driver']['givenName'] + " " +
                       drivers['Driver']['familyName']),
        )
        driver_data.save()
        i += 1


def tally():

    winner = RaceResults.objects.get(id=0)
    second = RaceResults.objects.get(id=1)
    third = RaceResults.objects.get(id=2)
    fourth = RaceResults.objects.get(id=3)
    fifth = RaceResults.objects.get(id=4)

    def addPoints(pos, points):
        pos = DriverStandingsModel.objects.get(full_name=pos)
        if user.racer.filter(full_name=pos).exists():
            user.points += points
            user.current_points += points
            user.save()
            user.correct += 1

    for user in UserModel.objects.all():
        addPoints(winner, 100)
        addPoints(second, 75)
        addPoints(third, 50)
        addPoints(fourth, 20)
        addPoints(fifth, 20)
        if user.correct == 5:
            if user.pitboss:

                update_message = UpdateNotification.objects.create(
                    update='You Kept Your Pitboss Streak Alive'

                )
            else:
                update_message = UpdateNotification.objects.create(
                    update='You Recieved The PitBoss Badge on' +

                    str(datetime.now().date())
                )

            user.pitboss = True
            user.save()

            Notification.objects.create(
                update=update_message,
                receiver=user,
                delete_update=update_message.id)

        else:

            user.pitboss = False

        user.correct = 0
        user.save()

        update_message = UpdateNotification.objects.create(
            update='Driver standings and points have been updated on ' +
            str(datetime.now().date())
        )

        Notification.objects.create(
            update=update_message,
            receiver=user,
            delete_update=update_message.id)

    maxPoints = UserModel.objects.all().order_by('-current_points')[0]

    for user in UserModel.objects.all():

        if user.current_points != maxPoints.current_points:
            user.wins = 0
        else:
            user.wins += 1

        if user.wins == 3:
            user.badge = True
            update_message = UpdateNotification.objects.create(
                update='You Recieved The HotStreak Badge on ' +
                str(datetime.now().date())
            )
        elif user.wins > 3:
            update_message = UpdateNotification.objects.create(
                update='You Kept your HotStreak alive ' +
                str(datetime.now().date())
            )

            Notification.objects.create(
                update=update_message,
                receiver=user,
                delete_update=update_message.id)
        else:
            user.badge = False

        user.current_points = 0
        user.save()


def leaderboard_view(request):
    all_users = UserModel.objects.order_by('-points')
    return render(request, 'leaderboard.html', {'all_users': all_users})
