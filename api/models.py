from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid

class UserManager(BaseUserManager):

    def create_user(self, email, password):
        if not email or not password:
            raise ValueError("Missing values")

        user = self.model(
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password):
        if not email or not password:
            raise TypeError("Missing values")
        
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name= 'email address',
        max_length=200,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = "login"

class UserProfile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(max_length=50, unique=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        db_table = "profile"

class Client(models.Model):

    repeat_choice = (
    ('none', 'None'),
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    )

    shift_option = (
    ('morning shift 5am to 9 am', 'Morning Shift - 5am to 9 am'),
    )

    day_option = (
    ('weekdays', 'Weekdays'),
    ('monday', 'Mon'),
    ('tuesday', 'Tue'),
    ('wednesday', 'Wed'),
    ('thursday', 'Thu'),
    ('friday', 'Fri'),
    ('saturday', 'Sat'),
    ('sunday', 'Sun'),
    )

    client_user = models.ForeignKey(User,on_delete= models.CASCADE)
    start_date = models.DateField(auto_now_add=False)
    arrival_time = models.TimeField(auto_now_add=False)
    departure_time = models.TimeField(auto_now_add=False)
    repeat = models.CharField(max_length=10,choices=repeat_choice)
    shift_available = models.CharField(max_length=50, choices=shift_option) 
    #doubt in weekdays
    day = models.CharField(max_length=20,choices=day_option)


    class Meta:
        db_table = "client"