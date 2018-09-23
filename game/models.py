from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from .__init__ import path


# Create your models here.
class Profile(models.Model):
    user_obj = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    bot_ext = models.CharField(max_length=5, default="cpp")
    bot_path = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=15)
    gwon = models.IntegerField(default=0)
    glost = models.IntegerField(default=0)
    gdrawn = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    college = models.CharField(max_length=100)

    def __str__(self):
        return self.user_obj.username + "-" + self.phone

    def create(self, **kwargs):
        user = User(username=kwargs["username"], email=kwargs["email"], first_name=kwargs["first_name"])
        user.set_password(kwargs["password"])
        user.save()
        self.user_obj = user
        self.phone = kwargs["phone"]
        self.college = kwargs["college"]

    def create_myuser(self, *args, **kwargs):  # Overriding default save method
        self.bot_path = path + "files/bot" + str(self.user_obj.pk)  # First set bot_path. No extension included
        print(self.bot_path)
        f = open(self.bot_path + '.' + self.bot_ext, 'w')
        f.close()
        try:
            super(Profile, self).save()  # Call default save method
        except:
            print("Exception occurred:")

    def total_score(self):
        self.points = (self.wins * 2) + (self.draws * 1)
        # self.wins

    def update(self):
        try:
            super(Profile, self).save()
        except:
            return False
        return True
