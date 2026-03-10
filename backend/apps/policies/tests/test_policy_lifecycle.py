import pytest, hashlib
from django.urls import reverse
from rest_framework.test import APIClient
from apps.captives.models import Captive
from apps.policies.models import Policy

pytestmark = pytest.mark.django_db

def test_policy_transition_and_export(tmp_path, broker_user, client: APIClient):
    client.force_authenticate(broker_user)
    captive = Captive.objects.create(name="C1", inception_date="2020-01-01")
    pol = Policy.objects.create(captive=captive, policy_number="P001",
                                effective_date="2024-01-01", expiry_date="2025-01-01",
                                premium=1000)

    # policy -> endorse
    url = reverse("policy-endorse", args=[pol.id])
    res = client.post(url, {"new_premium": 1200})
    assert res.status_code == 200
    assert res.data["status"] == "endorsed"

    # export excel
    url = reverse("policy-export", args=[pol.id])
    res = client.get(url)
    assert res.status_code == 200
    assert res['Content-Type'] == 'application/vnd.ms-excel'
    sha256 = res['X-SHA256']
    # Ensure stable export
    blob = b"".join(res.streaming_content)
    assert hashlib.sha256(blob).hexdigest() == sha256

    # Non-broker should 403
    url = reverse("policy-endorse", args=[pol.id])
    client.force_authenticate(User.objects.create_user(email="uw@example.com", password="pass"))
    res = client.post(url, {})
    assert res.status_code == 403
