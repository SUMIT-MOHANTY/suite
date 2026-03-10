import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def broker_user(db):
    return User.objects.create_user(email="broker@example.com", password="pass")

@pytest.fixture
def underwriter_user(db):
    return User.objects.create_user(email="uw@example.com", password="pass")
