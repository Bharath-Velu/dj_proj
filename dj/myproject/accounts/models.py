from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True , null=True , blank=True)
    is_email_verified =  models.BooleanField(default=False)

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        from datetime import timedelta, timezone , datetime
        return self.created_at >= datetime.now(timezone.utc) - timedelta(minutes=5)
