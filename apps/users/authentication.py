from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class AllowInactiveUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, reactivating=False, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password) and (user.is_active or reactivating):
                return user
        except UserModel.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        """
        Allow inactive users to authenticate for reactivation.
        """
        return True