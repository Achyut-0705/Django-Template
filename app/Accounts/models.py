from django.db import models
from django.core.validators import RegexValidator,MaxValueValidator,MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')
        if not password:
            raise ValueError('Users must have an password address')

        # username = self.normalize_username(username)
        # email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password, **extra_fields):
        # email = self.normalize_email(email)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        user = self.model( **extra_fields)
        user.set_password(password)
        user.status = "Approved"
        user.save()
        return user


class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('NB','Non-Binary')
    )

    ROLE_CHOICES = (
        ('SuperAdmin', 'Super Admin'),
        ('Admin', 'Admin'), 
        ('Staff', 'Staff')
    )

    USER_STATUS_CHOICES = (
        ('Approved', 'Approved'),
        ('Denied', 'Denied'),
        ('Pending', 'Pending')
    )

    email=None
    username = models.CharField(max_length=16, unique=True)
    address = models.CharField(max_length=256)
    mobile_no = models.CharField(max_length=64)
    date_of_birth = models.DateField(blank=True, null=True)
    role = models.CharField(_('role'), max_length=10, choices=ROLE_CHOICES, default="Staff")
    gender = models.CharField(_('gender'), max_length=2, choices=GENDER_CHOICES)
    status = models.CharField(_('status'), max_length=10, choices=USER_STATUS_CHOICES, default="Pending")
    approved_by = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    designation = models.CharField(max_length=50, null=True)
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        return self.username
        
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return '{0}'.format(filename)


class ProfileImage(models.Model):
    file = models.ImageField(upload_to = user_directory_path)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,blank=True, null=True,related_name='%(class)s_profile_image_created')
    uploaded_at = models.DateTimeField(auto_now_add=True)