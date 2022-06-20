from django.urls import path
from . import  views

urlpatterns = [
    # path('', views.index, name='index'),
    path('posts/user_id/<user_id>', views.user_post,name='posts'),
    path('vote/<user_id>', views.vote, name="vote"),
]
