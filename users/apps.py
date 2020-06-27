from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    # import signals inside the ready function
    def ready(self):
        import users.signals
