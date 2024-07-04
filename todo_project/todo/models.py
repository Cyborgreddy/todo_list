from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()

def get_default_user_id():
    return User.objects.first().id

class Task(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not started'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user_id)
    task = models.CharField(max_length=255)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')

    def check_and_update_status(self):
        if self.due_date < timezone.now().date() and self.status != 'completed':
            self.status = 'expired'

    def save(self, *args, **kwargs):
        self.check_and_update_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.task
