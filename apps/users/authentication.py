from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned

class AllowInactiveUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, reactivating=False, **kwargs):
        UserModel = get_user_model()
        # First, try to fetch the user by username
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # If the user is not found by username, try by email
            try:
                user = UserModel.objects.get(username=username)
            except (UserModel.DoesNotExist, MultipleObjectsReturned):
                # Return None if no user or multiple users are found with this email
                return None
            
        # Check the password (and whether the user is active, if applicable)
        if user.check_password(password) and (user.is_active or reactivating):
            return user

    def user_can_authenticate(self, user):
        """
        Allow inactive users to authenticate for reactivation.
        """
        return True