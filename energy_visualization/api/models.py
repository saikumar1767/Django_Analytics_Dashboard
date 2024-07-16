from django.db import models
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=100, null=False)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class EnergyData(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, to_field='username', db_column='username', on_delete=models.CASCADE)
    energy_source = models.CharField(max_length=50, null=False)
    consumption = models.FloatField(null=False)
    generation = models.FloatField(null=False)
    timestamp = models.DateTimeField(null=False, default=datetime.utcnow)
