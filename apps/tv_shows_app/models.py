from django.db import models
import datetime

class ShowsDataManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        # Title
        if len(postData['title']) < 2:
            errors["title"] = "Title name should be at least 2 characters"

        # Network
        if len(postData['network']) < 3:
            errors["network"] = "Network name should be at least 3 characters"

        # Description
        if postData['desc'] != None and len(postData['desc']) < 10:
            errors["Description"] = "Show description should be at least 10 characters"
        now = datetime.datetime.utcnow()

        #Release date
        if str(postData['release_date']) == "":
            errors["Release date"] = "Release date should not be empty."
        else: 
            if datetime.datetime.strptime(str(postData['release_date']), '%Y-%m-%d') >= now:
                errors["Release date"] = "date can't be in the future."

        return errors

class shows(models.Model):
    title = models.CharField(max_length=100)
    network = models.CharField(max_length=100)
    release_date = models.DateTimeField(auto_now_add=False)
    desc = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    objects = ShowsDataManager()
# Create your models here.

def __repr__(self):
    return f("shows: {self.title}, {self.network}, {self.release_date}}")
