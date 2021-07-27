"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.contrib import admin

from raceapi.views import get_standings, leaderboard_view
from notification.views import (delete_like, delete_notification,
                                delete_update, notification_view,
                                delete_follow, delete_comment)
from authentication.views import CreateUser, LoginUser, logout_user
from appuser.views import (EditUserProfile, remove_driver, unfollow_user,
                           follow_user, get_user_profile, user_drivers,
                           followers, following, add_driver)
from post.views import (PostDetailView, delete_comments, delete_post,
                        index, post, PostLike,
                        CommentLike, Test_view)


urlpatterns = [
    path('test/', Test_view, name='Test'),
    path('admin/', admin.site.urls),
    path('sign_up/', CreateUser.as_view(), name='create_user'),
    path('login/', LoginUser.as_view(), name='login_page'),
    path('logout/', logout_user),
    path('post/', post),
    path('post/<int:post_id>/', PostDetailView),
    path('like/<int:pk>/comment/', CommentLike, name="comment_like"),
    path('', index, name='homepage'),
    path('like/<int:pk>/', PostLike, name="post_like"),
    path('notification/<int:user_id>/',
         notification_view, name="notification"),
    path('delete_notifications/<int:id>/',
         delete_notification, name="delete_noti"),
    path('standings/', get_standings, name='standings'),
    # user profile links
    path('profile/<int:user_id>/edit/',
         EditUserProfile.as_view(), name='edit_profile'),
    path('profile/<int:user_id>/follow/', follow_user, name='follow'),
    path('profile/<int:user_id>/unfollow/', unfollow_user, name='unfollow'),
    path('profile/<int:user_id>/', get_user_profile, name='profile'),
    path('profile/<int:user_id>/racers/', user_drivers),
    path('profile/<int:user_id>/followers/', followers),
    path('profile/<int:user_id>/following/', following),
    path('delete_follow/<int:id>/',
         delete_follow, name="delete_follow"),
    path('standings/<int:user_id>/add_driver/', add_driver),
    path('standings/<int:user_id>/remove_driver/', remove_driver),
    path('delete_update/<int:id>/',
         delete_update, name="delete_update"),
    path('delete_comment/<int:id>/',
         delete_comment, name="delete_comment"),
    path('delete_post/<int:pk>/',
         delete_post, name="delete_post"),
    path('delete_comments/<int:pk>/',
         delete_comments, name="delete_comments"),
    path('delete_like/<int:id>/',
         delete_like, name="delete_likes"),
    path('leaderboard/', leaderboard_view, name='leaderboard')

]


urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
