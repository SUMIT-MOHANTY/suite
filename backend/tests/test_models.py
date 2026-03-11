import pytest
from tests.factories import CaptiveFactory, PolicyFactory, ClaimFactory, ContactFactory

@pytest.mark.django_db
def test_captive_unique_name_jurisdiction():
    c1 = CaptiveFactory(name="Test1", jurisdiction="CYM")
    pytest.raises(Exception, CaptiveFactory, name="Test1", jurisdiction="CYM")

@pytest.mark.django_db
def test_policy_unique_policy_number():
    PolicyFactory(policy_number="XYZ")
    pytest.raises(Exception, PolicyFactory, policy_number="XYZ")

@pytest.mark.django_db
def test_cascade_delete_policy():
    captive = CaptiveFactory()
    policy = PolicyFactory(captive=captive)
    assert captive.policies.exists()
    captive.delete()
    assert not policy.__class__.objects.filter(id=policy.id).exists()

@pytest.mark.django_db
def test_contact_create():
    c = ContactFactory(email="unique@example.com")
    assert c.role == "OTHER"
