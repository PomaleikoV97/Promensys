from django.contrib.auth.backends import BaseBackend

from project.models import RegistredUser


class PhoneNumberBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = RegistredUser.objects.get(phone=phone)
        except RegistredUser.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return RegistredUser.objects.get(pk=user_id)
        except RegistredUser.DoesNotExist:
            return None
