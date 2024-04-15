from django.db import models


class Candidate(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField()
    party_affiliation = models.CharField(max_length=100)
    list_number = models.IntegerField(blank=True, null=True)
