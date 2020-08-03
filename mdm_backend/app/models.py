from django.db import models
from datetime import datetime
# Create your models here.


class Admin(models.Model):
  id = models.AutoField(primary_key=True, null=False)
  name = models.TextField()
  email = models.EmailField(null=False)
  password = models.TextField(null=False)

class School(models.Model):
  id = models.AutoField(primary_key=True, null=False)
  name = models.TextField()
  email = models.EmailField(null=False)
  password = models.TextField(null=False)
  api_key = models.TextField()
  net_id = models.TextField()
  mv_serial = models.TextField()
  server_ip = models.TextField()


class DailyTrue(models.Model):
  id = models.AutoField(primary_key=True, null=False)
  date = models.DateField(null=False, default=datetime.now)
  school = models.ForeignKey(School, on_delete=models.CASCADE)
  attendance_true = models.TextField(null=False)
  food_true = models.TextField(null=False)

class DailyPrediction(models.Model):
  id = models.AutoField(primary_key=True, null=False)
  date = models.DateField(default=datetime.now, null=False)
  school = models.ForeignKey(School, on_delete=models.CASCADE)
  attendance_pred = models.TextField(null=False)
  food_pred = models.TextField(null=False)

class Reports(models.Model):
  id = models.AutoField(primary_key=True, null=False)
  school = models.ForeignKey(School, on_delete=models.CASCADE)
  date = models.DateField(null=False, default=datetime.now)
  true = models.ForeignKey(DailyTrue, on_delete=models.CASCADE)
  pred = models.ForeignKey(DailyPrediction, on_delete=models.CASCADE)
  acc = models.TextField()
  is_discrepancy = models.TextField()

class Discrepancy(models.Model):
  id = models.AutoField(primary_key=True, null=False)
  report = models.ForeignKey(Reports, on_delete=models.CASCADE)
  assign_to = models.ForeignKey(Admin, on_delete=models.CASCADE)
  is_active = models.TextField()
