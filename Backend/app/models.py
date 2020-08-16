from django.db import models
import hashlib


class OperationManager(models.Model):
    username = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=10)
    password = models.CharField(max_length=1000)

    def save(self, *args, **kwargs):
        m = hashlib.md5()
        m.update(self.password.encode("utf-8"))
        self.password = str(m.digest())
        super().save(*args, **kwargs)


class Mobilizer(models.Model):
    username = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=10)
    password = models.CharField(max_length=1000)
    om_id = models.ForeignKey(OperationManager, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.phone_no + '|' + str(id)

    def save(self, *args, **kwargs):
        m = hashlib.md5()
        m.update(self.password.encode("utf-8"))
        self.password = str(m.digest())
        super().save(*args, **kwargs)


class CustomToken(models.Model):
    token = models.CharField(max_length=500)
    object_id = models.IntegerField()
    user_type = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
    name = models.CharField(max_length=50)
    area = models.CharField(max_length=200)
    participants = models.IntegerField(default=0)
    scheduledTime = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(null=True)
    description = models.TextField(null=True)
    filename = models.CharField(max_length=200, null=True)
    status = models.CharField(default="Not Completed", max_length=100)
    mobiliser_id = models.ForeignKey(Mobilizer, on_delete=models.CASCADE)


class Students(models.Model):
    username = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=10)
    is_converted = models.BooleanField(default=False)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100, null=True)
    mobiliser_id = models.ForeignKey(Mobilizer, on_delete=models.CASCADE)
