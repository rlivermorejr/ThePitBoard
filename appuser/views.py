from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages

from appuser.forms import EditProfile
from appuser.models import UserModel, RacerList
from post.models import Post
from notification.models import FollowNotification, Notification
from raceapi.models import DriverStandingsModel


def get_user_profile(request, user_id: int):
    """
    Displays user profile and also checks
    for existing user in case you manually
    type the address in the url
    """
    count = len(
        [notified for notified in Notification.objects.filter(
            receiver__id=request.user.id)])

    try:
        account = UserModel.objects.get(id=user_id)
        racers = DriverStandingsModel.objects.filter()
    # cur_user = Account.objects.get(id=request.user.id)
    except UserModel.DoesNotExist:
        messages.info(request, "This account does not exist!")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # return HttpResponseRedirect(reverse('main'))
    return render(request, 'profile.html', {'account': account, 'count': count})


def user_drivers(request, user_id: int):
    account = UserModel.objects.get(id=user_id)
    drivers = account.racer.all()
    if drivers is None:
        drivers = None
        return render(request, 'user_drivers.html', {'drivers': drivers})
    return render(request, 'user_drivers.html', {'drivers': drivers})


def followers(request, user_id: int):
    """
    Shows all of the followers from the profile
    you are currently viewing
    """
    try:
        account = UserModel.objects.get(id=user_id)
        follow = account.followers.all()
    except UserModel.DoesNotExist:
        messages.info(request, "This account does not exist!")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return render(request, 'user_follow.html', {'follow': follow})


def following(request, user_id: int):
    """
    Shows all of the users being followed
    by the user of the profile you are
    currently viewing
    """
    try:
        account = UserModel.objects.get(id=user_id)
        follow = account.following.all()
    except UserModel.DoesNotExist:
        messages.info(request, "This account does not exist!")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return render(request, 'user_follow.html', {'follow': follow})


@login_required
def follow_user(request, user_id: int):
    """
    Will check that you are not currently following
    the other user and will also check if
    the user is yourself
    """
    cur_user = UserModel.objects.get(id=request.user.id)
    follow = UserModel.objects.get(id=user_id)
    if follow.id == cur_user.id:
        messages.info(request, "You cannot follow yourself!")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    if not follow.followers.filter(username=cur_user.username).exists():
        cur_user.following.add(follow)
        cur_user.save()
        follow.followers.add(cur_user)
        follow.save()

        new_message = FollowNotification.objects.create(
            message=request.user,
            user_id=cur_user.id
        )

        Notification.objects.create(
            message=new_message,
            receiver=UserModel.objects.get(username=follow),
            delete_message=new_message.id
        )

        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        messages.info(request, "You're already following this person!")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def unfollow_user(request, user_id):
    """
    Makes sure you are actually following
    the other user. It will also check
    to make sure the other user is not
    yourself
    """
    cur_user = UserModel.objects.get(id=request.user.id)
    unfollow = UserModel.objects.get(id=user_id)
    if unfollow.id == cur_user.id:
        messages.info(request, "You're not following yourself!")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    if unfollow.followers.filter(username=cur_user.username).exists():
        cur_user.following.remove(unfollow)
        unfollow.followers.remove(cur_user)
        unfollow.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        messages.info(request, "You're not following this person!")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class EditUserProfile(View):
    def get(self, request, user_id):
        count = len(
            [notified for notified in Notification.objects.filter(
                receiver__id=request.user.id)])

        cur_user = UserModel.objects.get(id=user_id)
        form = EditProfile(initial={
            # 'username': cur_user.username,
            'bio': cur_user.bio,
            'date_of_birth': cur_user.date_of_birth,
            'profile_image': cur_user.profile_image
        })
        return render(request, 'generic_form.html',
                      {'form': form, 'count': count})

    def post(self, request, user_id):
        cur_user = UserModel.objects.get(id=user_id)
        form = EditProfile(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            if 'static' not in data['profile_image']:
                cur_user.profile_image = data['profile_image']
            cur_user.bio = data['bio']
            cur_user.date_of_birth = data['date_of_birth']
            cur_user.save()
            return render(request, 'profile.html', {'account': cur_user})
        else:
            message = form.errors
            return render(request, 'profile.html', {'account': cur_user,
                                                    'message': message})


@login_required
def add_driver(request, user_id):
    cur_user = UserModel.objects.get(id=request.user.id)
    driver = DriverStandingsModel.objects.get(id=user_id)
    add = RacerList.objects.get(full_name=driver)
    cur_user.racer.add(add)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def remove_driver(request, user_id):
    cur_user = UserModel.objects.get(id=request.user.id)
    driver = DriverStandingsModel.objects.get(id=user_id)

    remove = RacerList.objects.get(full_name=driver.full_name)
    cur_user.racer.remove(remove)
    cur_user.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
