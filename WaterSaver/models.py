# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Test(models.Model):
    test = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'test'
        app_label = 'WaterSaver'


class Waterdata(models.Model):
    starttimeepoch = models.BigIntegerField(db_column='startTimeEpoch')  # Field name made lowercase.
    stoptimeepoch = models.BigIntegerField(db_column='stopTimeEpoch')  # Field name made lowercase.
    averagewaterflowrate = models.FloatField(db_column='averageWaterFlowRate')  # Field name made lowercase.
    waterflowreadingstotal = models.FloatField(db_column='waterFlowReadingsTotal')  # Field name made lowercase.
    numberofwaterflowreadings = models.IntegerField(db_column='numberOfWaterFlowReadings')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'waterData'
        app_label = 'WaterSaver'
