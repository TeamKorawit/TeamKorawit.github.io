from django.conf import settings
from django.db import models

class Availability(models.Model):
    ALL_DAY = 'ALL'
    STATUS_AVAILABLE = 'AVAILABLE'
    STATUS_UNAVAILABLE = 'UNAVAILABLE'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField(db_index=True)
    time_slot = models.CharField(max_length=64, default=ALL_DAY)
    status = models.CharField(max_length=12, choices=[(STATUS_AVAILABLE,'Available'), (STATUS_UNAVAILABLE,'Unavailable')])
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user','date','time_slot')
        ordering = ['date']

    def __str__(self):
        return f"{self.user} - {self.date} {self.time_slot} {self.status}"
