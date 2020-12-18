from django.db import models


class BBSORecords(models.Model):
    location_details = models.CharField(blank=True, help_text='e.g. In the kitchen on the 4th floor.', max_length=50)
    PTW = models.CharField(blank=True, max_length=10, verbose_name='Permit To Work Number')
    JSA = models.CharField(blank=True, max_length=10, verbose_name='Job Safety Analysis Number')
    details_of_observation = models.TextField()


class BBSORecordActions(models.Model):
    bbso_record_ID = models.ForeignKey(BBSORecords, on_delete=models.CASCADE, related_name='records', verbose_name='BBSO Record')
    recommended_action = models.TextField(verbose_name='Recommended Action')
