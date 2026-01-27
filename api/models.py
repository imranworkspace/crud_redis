from django.db import models

class StudentModel(models.Model):
    username = models.CharField(max_length=25)
    email = models.EmailField(max_length=25,unique=True)

    def __str__(self):
        return self.username