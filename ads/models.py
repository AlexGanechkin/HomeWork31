from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    lat = models.DecimalField("Латтитуда", max_digits=8, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField("Лонгитуда", max_digits=8, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'


class UserRoles(models.TextChoices):
    MEMBER = 'member', 'Пользователь'
    MODERATOR = 'moderator', 'Модератор'
    ADMIN = 'admin', 'Администратор'


class User(AbstractUser):
    first_name = models.CharField("Имя", max_length=150, blank=True)  # от наставника: можно удалить, т.к. есть в базовой модели
    last_name = models.CharField(max_length=150, verbose_name="Фамилия", blank=True)
    username = models.CharField("Никнейм", max_length=100, unique=True)
    password = models.CharField("Пароль", max_length=128)
    role = models.CharField(choices=UserRoles.choices, max_length=9, default='member')
    age = models.PositiveSmallIntegerField(null=True)
    location_id = models.ManyToManyField(Location)


    # Еще один вариант от наставника по созданию хешированного пароля
    #def save(self, *args, **kwargs):
    #    self.set_password(raw_password=self.password)
    #    super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ["username"]


class Publication(models.Model):
    name = models.CharField(max_length=200)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.PositiveIntegerField()
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to='logos/')
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Selection(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Publication)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'