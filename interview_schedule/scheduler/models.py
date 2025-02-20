from django.db import models
from django.utils import timezone

# Create your models here.
class UserDetails(models.Model):

    user_id = models.CharField(max_length=30, unique=True, primary_key = True)
    user_name = models.CharField(max_length=40, default="", unique=True)
    user_type = models.CharField(max_length=30,default="")
    user_mail = models.EmailField(default="",unique=True, null=False)
    time_slot_from = models.IntegerField(default="")
    time_slot_to = models.IntegerField(default="")
    created_at = models.DateTimeField(default=timezone.now,blank=True)

    class Meta:
        db_table = 'user_details'