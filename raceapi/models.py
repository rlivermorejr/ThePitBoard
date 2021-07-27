from django.db import models

"""
Model that is filled with data pulled from the API.
"""


class DriverStandingsModel(models.Model):
    id = models.AutoField(primary_key=True)

    given_name = models.CharField(max_length=100, blank=True, null=True)
    family_name = models.CharField(max_length=100, blank=True, null=True)
    dob = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=200, blank=True, null=True)
    code = models.CharField(max_length=5, blank=True, null=True)
    permanent_number = models.CharField(max_length=500, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    points = models.IntegerField(default=0)
    wins = models.CharField(max_length=50, blank=True, null=True)
    constructor_name = models.CharField(max_length=100, blank=True, null=True)
    cons_nat = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.full_name


class RaceResults(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.full_name
