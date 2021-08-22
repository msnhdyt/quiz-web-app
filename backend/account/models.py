from enum import unique
from django.db.models.base import Model
from topic.models import Topic
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from quizzes.models import Quizzes

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, account_type, password=None):
        if not email:
            raise ValueError("email is required")
        if not first_name:
            raise ValueError("first name is required")
        if not last_name:
            raise ValueError("last name is required")
        if not account_type:
            raise ValueError("account type is required")
        
        user = self.model(
             email= self.normalize_email(email),
             first_name = first_name,
             last_name = last_name,
             account_type = account_type
         )
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, first_name, last_name, account_type, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            password = password,
            account_type=account_type
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    account_type_choices = [
        ('O', 'others'),
        ('S', 'student'),
        ('T', 'teacher')
    ]
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=1, choices=account_type_choices, default='O')
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_topic = models.ManyToManyField(Topic, through='usertopic')
    quiz_taken = models.ManyToManyField(Quizzes, through='takequiz')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'account_type']

    objects = MyUserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

# class UserProfile(models.Model):
#     account_type_choices = [
#         ('O', 'others'),
#         ('S', 'student'),
#         ('T', 'teacher')
#     ]

#     id = models.CharField(primary_key=True, max_length=8, unique=True)
#     name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100, unique=True)
#     account_type = models.CharField(max_length=1, choices=account_type_choices, default='O')
#     user_topic = models.ManyToManyField(Topic, through='usertopic')
#     quiz_taken = models.ManyToManyField(Quizzes, through='takequiz')

class UserTopic(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, db_constraint=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, db_constraint=False)
    date_joined = models.DateTimeField()

class TakeQuiz(models.Model):
    id = models.CharField(max_length=20, primary_key=True, unique=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, db_constraint=False)
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE, db_constraint=False)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now=True)
    similarity = models.FloatField(null=True)
    score = models.FloatField(null=True)

