from datetime import date

from rest_framework.exceptions import ValidationError


def check_not_published(value):
    if value:
        raise ValidationError("Нельзя создавать опубликованные объявления!")


def check_birth_date(birth_date):
    age = (date.today().year - birth_date.year - 1) + ((date.today().month, date.today().day) >= (birth_date.month, birth_date.day))
    if age < 9:
        raise ValidationError("Возраст пользователя должен быть более 9 лет!")


def check_email(email):
    if "rambler.ru" in email:
        raise ValidationError("С домена rambler регистрация запрещена!")
