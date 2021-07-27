from django.db import models
from post.models import Post, Comment
from appuser.models import UserModel


class FollowNotification(models.Model):
    message = models.CharField(max_length=50)
    user_id = models.IntegerField(default=0)


class UpdateNotification(models.Model):
    update = models.CharField(max_length=100)


class LikeNotification(models.Model):
    liked = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Notification(models.Model):
    receiver = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="receiver")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_received",
        null=True, blank=True)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="comment_received",
        null=True, blank=True)
    message = models.ForeignKey(
        FollowNotification, on_delete=models.CASCADE, related_name="message_received",
        null=True, blank=True)

    update = models.ForeignKey(
        UpdateNotification, on_delete=models.CASCADE, related_name='new_update', null=True, blank=True)
    liked = models.ForeignKey(LikeNotification, on_delete=models.CASCADE,
                              related_name='like_recieved', null=True, blank=True)
    delete_id = models.IntegerField(null=True, blank=True)
    viewed_at = models.DateTimeField(default=None, blank=True, null=True)
    delete_message = models.IntegerField(null=True, blank=True)
    delete_update = models.IntegerField(null=True, blank=True)
    delete_comment = models.CharField(
        max_length=270, null=True, blank=True)
    delete_like = models.IntegerField(null=True, blank=True)
