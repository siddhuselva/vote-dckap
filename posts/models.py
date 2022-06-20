from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=32)

    def __str__(self):
        return self.user_name


# Create your models here.
class Post(models.Model):

    post = models.CharField(max_length=250, default='')
    title = models.CharField(max_length=32, default='')
    up_vote = models.IntegerField(default=0)
    down_vote = models.IntegerField(default=0)
    user_vote = models.ManyToManyField(User, related_name='user_vote', default=None, blank=True)

    def __str__(self):
        return self.title


class Vote(models.Model):
    post = models.ForeignKey(Post, related_name="postid", on_delete=models.CASCADE, default=None, blank=True)
    vote = models.BooleanField(default=True)
    user = models.ForeignKey(User, related_name="userid", on_delete=models.CASCADE, default=None, blank=True)
    # vote_type = models.BooleanField(null=True)

    def __str__(self):
        return str(self.vote)
