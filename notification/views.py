from django.contrib.auth.decorators import login_required
from django.utils import timezone
from notification.models import Notification
from django.shortcuts import redirect, render


@login_required
def notification_view(request, user_id):
    count = len(
        [notified for notified in Notification.objects.filter(
            receiver__id=request.user.id)])

    notifications = Notification.objects.filter(receiver__id=user_id)
    notification = []
    for notified in notifications:

        notification.append(notified.post)
        notification.append(notified.message)
        notification.append(notified.update)
        notification.append(notified.comment)
        notification.append(notified.liked)
        notified.viewed_at = timezone.now()

        notified.save()

    return render(request, "notification_view.html",
                  {"notification": notification[::-1], 'count': count})


def delete_notification(request, id):
    Notification.objects.filter(delete_id=id).delete()

    return redirect(request.META.get('HTTP_REFERER',
                                     'redirect_if_referer_not_found'))


def delete_follow(request, id):
    Notification.objects.filter(delete_message=id).delete()
    return redirect(request.META.get('HTTP_REFERER',
                                     'redirect_if_referer_not_found'))


def delete_update(request, id):
    Notification.objects.filter(delete_update=id).delete()
    return redirect(request.META.get('HTTP_REFERER',
                                     'redirect_if_referer_not_found'))


def delete_comment(request, id):
    Notification.objects.filter(delete_comment=id).delete()
    return redirect(request.META.get('HTTP_REFERER',
                                     'redirect_if_referer_not_found'))


def delete_like(request, id):
    Notification.objects.filter(delete_like=id).delete()
    return redirect(request.META.get('HTTP_REFERER',
                                     'redirect_if_referer_not_found'))
