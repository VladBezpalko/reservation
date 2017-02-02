from pytest import fixture

from pytest_django.lazy_django import skip_if_no_django

from django.contrib.auth import get_user_model

User = get_user_model()

pytest_plugins = ['date_fixtures', 'reservation_fixtures']


@fixture
def api_client():
    """A Django Rest Framework test client instance."""
    skip_if_no_django()

    from rest_framework.test import APIClient

    return APIClient()


@fixture
def api_rf():
    """APIRequestFactory instance."""
    skip_if_no_django()

    from rest_framework.test import APIRequestFactory

    return APIRequestFactory()


@fixture
def fixt_user(db):
    user = User.objects.create(
        email='joe@localhost',
        username='john',
    )
    return user


@fixture
def fixt_admin(db):
    return User.objects.create(
        email='admin@localhost',
        username='Admin',
        is_staff=True,
    )


@fixture
def api_user(api_client, fixt_user):
    api_client.force_authenticate(user=fixt_user)
    return api_client


@fixture
def api_admin(api_client, fixt_admin):
    api_client.force_authenticate(user=fixt_admin)
    return api_client
