from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings 

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ("staff", "Staff"),
        ("community", "Community"),
    ]
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default="community",
        help_text="Determines if the user is staff (admin) or a community member."
    )

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
        
    def save(self, *args, **kwargs):
        if self.user_type == "staff":
            self.is_staff = True
        super().save(*args, **kwargs)
