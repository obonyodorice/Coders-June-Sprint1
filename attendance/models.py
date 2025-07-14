from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings


class Attendance(models.Model):
    CHECK_STATUS = (
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
    )
    ROLE_CHOICES = (
        ('attachee', 'Attachee'),
        ('visitor', 'Visitor'),
        ('member', 'Member'),
        ('staff', 'Staff'),
        ('not_sure', 'Not Sure'),
    )
    DEPARTMENT_CHOICES = (
        ('communication', 'Communication'),
        ('creatives', 'Creatives'),
        ('tech', 'Tech Department'),
        ('youth_engagement', 'Youth Engagement'),
        ('heritage', 'Heritage'),
        ('admin', 'Admin'),
        ('finance', 'Finance'),
        ('entrepreneurship', 'Entrepreneurship'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendances"
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        null=False,
        blank=False
    )
    department = models.CharField(
        max_length=30,
        choices=DEPARTMENT_CHOICES,
        null=False,
        blank=False
    )
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=CHECK_STATUS, default='checked_in')
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date', 'user']

    def __str__(self):
        return f"{self.user.username} | {self.date} | {self.status} | {self.role} | {self.department}"
