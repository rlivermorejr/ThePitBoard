from django.db import models
from django.utils import timezone
from appuser.models import UserModel
from django_resized import ResizedImageField


from django.contrib.auth import get_user_model
User = get_user_model()


class Post(models.Model):
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(UserModel, related_name='post_like')
    liked = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    commenters = models.ManyToManyField(UserModel, related_name='commenters')
    post_content = models.ImageField(ResizedImageField(size=[400, 400],
                                                       upload_to='post_image',
                                                       quality=99, null=True, blank=True))

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.text


class Comment(models.Model):
    replied_to = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)

    comment = models.CharField(max_length=140)

    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(UserModel, related_name='comment_like')
    liked = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
