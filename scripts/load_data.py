from django.contrib.auth import get_user_model


def run():
    User = get_user_model()
    if not User.objects.filter(username="root").exists():
        User.objects.create_superuser(
            username="root", email="root@localhost", password="superman"
        )
