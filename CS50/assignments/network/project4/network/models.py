from sqlite3 import Timestamp
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Account(models.Model):
    bio = models.CharField(max_length=1000, default = 'No bie provided')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    followers = models.ManyToManyField(User, blank = True, null = True, related_name="followers")
    following = models.ManyToManyField(User, blank = True, null = True, related_name= "following")
    pictureurl = models.CharField(max_length=1000,default="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/SNice.svg/1200px-SNice.svg.png")
    def serialize(self):
        return {
            "id": self.id,
            "owner": self.owner.id,
            "followers": [follower.id for follower in self.followers.all()],
            "following": [following.id for following in self.following.all()],
            "pictureurl": self.pictureurl,
        }


class Comment(models.Model):
    content = models.CharField(max_length = 1000, default = "", blank=True)
    commener = models.ForeignKey(Account, on_delete=models.CASCADE, null = True, blank = True)


class Post(models.Model):
    poster = models.ForeignKey(Account, on_delete = models.CASCADE, related_name="poster")
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length = 1000, default = "", blank = True)
    likes = models.ManyToManyField(Account, default = [])
    comments = models.ManyToManyField(Comment, default = [])

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.id,
            "user": self.poster.owner.username,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "message": self.message,
            "likes": [like.owner.id for like in self.likes.all()],
            "comments": [{"commenter" : comment.commenter.owner.id, "comment": comment.content} for comment in self.comments.all()], 
        }