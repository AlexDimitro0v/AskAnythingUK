from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


# We have to create token that will be used in the email confirmation url upon registering. (Security measure)
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()
