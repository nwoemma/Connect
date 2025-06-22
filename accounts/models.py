from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.
class UserManger(BaseUserManager):
    def create_user(self, username, email=None, password=None):
        """
        Create a superuser with the given username, email, and password.
        """
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email=None, password=None):
        extra_fields = {
            "is_staff":True,
            "is_superuser":True,
        }
        extra_fields.setdefault(["is_staff", "is_super_user"], True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    STATUS = (
        ('del', 'deleted'),
        ('0','inactive'),
        ('1', 'active'),
        ('2', 'unverified')
    )
    ROLE = (
        ('Worker','Worker'),
        ('Customer','Customer'),
        ("Admin",'Admin'),
    )
    SEX_CHOICES = (
        ('male','Male'),
        ('female', 'Female')
    )
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_num= models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=13, choices=ROLE,null=True, blank=True)
    profile_pic= models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    password2 = models.CharField(max_length=128, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS, default='0')
    date_joined = models.DateTimeField(auto_now_add=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True)

    objects = UserManger()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_num']
    
    def get_full_name(self):
        full_name = f"{self.first_name + self.last_name}" 
        return full_name.capitalize() 
    
class OTP(models.Model):
    otp = models.CharField(max_length=9)
    phone = models.CharField(max_length=15)
    date_created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField("Expires")
    
    class Meta:
        db_table = 'otp_db_table'
        