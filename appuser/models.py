from django.db import models
from django.contrib.auth.models import AbstractUser

F1_DRIVER_CHOICES = [
    ('RIC', 'Daniel Riccairdo'),
    ('NOR', 'Lando Norris'),
    ('VET', 'Sebastian Vettel'),
    ('LAT', 'Nicholas Latifi'),
    ('RAI', 'Kimi Raikkonen'),
    ('MAZ', 'Nikita Mazepin'),
    ('GAS', 'Pierre Gasly'),
    ('PER', 'Sergio Perez'),
    ('ALO', 'Fernando Alonso'),
    ('LEC', 'Charles Leclerc'),
    ('STR', 'Lance Stroll'),
    ('TSU', 'Yuki Tsunoda'),
    ('OCO', 'Esteban Ocon'),
    ('VER', 'Max Verstappen'),
    ('HAM', 'Lewis Hamilton'),
    ('SCH', 'Mick Schumacher'),
    ('SAI', 'Carlos Sainz Jr.'),
    ('RUS', 'George Russell'),
    ('BOT', 'Valtteri Bottas'),
    ('GIO', 'Antonio Giovinazzi'),
]

pimg = '../static/images/profile_img.png'


class RacerList(models.Model):

    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class UserModel(AbstractUser):
    bio = models.CharField(max_length=250, default='I is racecar.')
    created_at = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(
        auto_now=False, default='1990-01-01')

    profile_image = models.ImageField(
        default=pimg, upload_to='profile_images/', blank=True)
    points = models.IntegerField(default=0)
    likes = models.ManyToManyField('self', symmetrical=False,
                                   blank=True,
                                   related_name='user_likes')
    followers = models.ManyToManyField('self', symmetrical=False,
                                       related_name='auth_followers',
                                       blank=True)
    following = models.ManyToManyField('self', symmetrical=False,
                                       related_name='auth_following',
                                       blank=True)
    racer = models.ManyToManyField(RacerList, blank=True)
    badge = models.BooleanField(default=False)
    correct = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    current_points = models.IntegerField(default=0)
    pitboss = models.BooleanField(default=False)

    def __str__(self):
        return self.username
