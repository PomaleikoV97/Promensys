from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import jwt

from promensys import settings


class UserManager(BaseUserManager):
    def create_user(self, password, phone,
                    is_admin=False, is_staff=False,
                    is_active=False, is_superuser=False,
                    login=''):

        if not phone:
            raise ValueError("User must have phone")
        if not password:
            raise ValueError("User must have password")

        user = self.model(phone=phone)
        user.set_password(password)
        user.login = login
        user.is_admin = is_admin
        user.is_staff = is_staff
        user.is_active = is_active
        user.is_superuser = is_superuser
        user.save()

        return user


    def create_superuser(self, password, phone):
        if not phone:
            raise ValueError("User must have phone")
        if not password:
            raise ValueError("User must have password")

        user = self.create_user(password=password, phone=phone)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.is_active = True
        user.save()

        return user


    def check_password(self, user, password):
        return user.check_password(password)


class RegistredUser(AbstractUser):
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    username = None
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, default='M')
    email = models.EmailField()
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=13, unique=True)
    login = models.CharField(max_length=200)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    def __str__(self):
        return self.phone


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория', db_index=True)
    user = models.ForeignKey(RegistredUser, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Project(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', null=True, verbose_name='Добавить фотографию')
    user = models.ForeignKey(RegistredUser, verbose_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    deadline = models.DateField(null=True, blank=True, verbose_name='Крайний срок выполнения')
    completed = models.BooleanField(default=False, blank=True, verbose_name='Выполнено')
    project = models.ForeignKey(Project, verbose_name='Проект', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', null=True, verbose_name='Добавить фотографию')
    user = models.ForeignKey(RegistredUser, verbose_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title

