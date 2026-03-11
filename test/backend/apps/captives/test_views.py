import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from backend.apps.captives.models import CaptiveModel

User = get_user_model()


@pytest.fixture
def api_client():
    """API client for testing"""
    return APIClient()


@pytest.fixture
def sample_captive():
    """Sample captive fixture"""
    return CaptiveModel.objects.create(
        name="Sample Captive Co.",
        jurisdiction="CAY",
        formation_date="2023-06-01",
        minimum_capital=1000000,
        paid_up_capital=500000,
        surplus=200000,
    )


@pytest.fixture
def auth_user():
    """Authenticated user"""
    return User.objects.create_user(username="testuser", password="testpass")


def test_post_create_captive(api_client):
    """Test POST /api/captives creates a new captive"""
    url = reverse("captive-list")
    payload = {
        "name": "New Captive Inc.",
        "jurisdiction": "AVG",
        "formation_date": "2024-01-15",
        "minimum_capital": 500000,
        "paid_up_capital": 250000,
        "surplus": 50000,
    }
    response = api_client.post(url, payload, format="json")
    
    assert response.status_code == 201
    assert response.data["name"] == payload["name"]
    assert response.data["min_capital_surplus"] == 550000
    assert "id" in response.data
    assert response.data["created_at"] is not None


def test_patch_update_captive(api_client, sample_captive):
    """Test PATCH /api/captives/:id updates specific fields"""
    url = reverse("captive-detail", kwargs={"pk": sample_captive.pk})
    payload = {"surplus": 60000}
    response = api_client.patch(url, payload, format="json")
    
    assert response.status_code == 200
    assert response.data["min_capital_surplus"] == 1060000  # 1000000 + 60000
    sample_captive.refresh_from_db()
    assert sample_captive.surplus == 60000


def test_get_single_captive(api_client, sample_captive):
    """Test GET /api/captives/:id returns captive details"""
    url = reverse("captive-detail", kwargs={"pk": sample_captive.pk})
    response = api_client.get(url)
    
    assert response.status_code == 200
    assert response.data["id"] == sample_captive.pk
    assert response.data["name"] == sample_captive.name
    assert response.data["min_capital_surplus"] == 1200000


def test_get_list_captives(api_client, sample_captive):
    """Test GET /api/captives returns paginated list"""
    url = reverse("captive-list")
    response = api_client.get(url)
    
    assert response.status_code == 200
    assert "results" in response.data
    assert isinstance(response.data["results"], list)
    assert response.data["results"][0]["policy_count"] == 0


def test_400_error_on_constraint(api_client):
    """Test 400 error when validation constraint fails"""
    url = reverse("captive-list")
    payload = {
        "name": "Bad Captive",
        "jurisdiction": "BER",
        "formation_date": "2024-01-15",
        "minimum_capital": 1000,
        "paid_up_capital": 2000,  # Invalid: exceeds minimum
        "surplus": 500,
    }
    response = api_client.post(url, payload, format="json")
    
    assert response.status_code == 400
    assert "paid_up_capital" in response.data


def test_404_error_on_bad_id(api_client):
    """Test 404 for non-existent captive ID"""
    url = reverse("captive-detail", kwargs={"pk": 99999})
    response = api_client.get(url)
    
    assert response.status_code == 404


def test_delete_204(api_client, sample_captive):
    """Test DELETE /api/captives/:id removes captive"""
    url = reverse("captive-detail", kwargs={"pk": sample_captive.pk})
    response = api_client.delete(url)
    
    assert response.status_code == 204
    assert not CaptiveModel.objects.filter(pk=sample_captive.pk).exists()


def test_put_update_entire_captive(api_client, sample_captive):
    """Test PUT /api/captives/:id updates all fields"""
    url = reverse("captive-detail", kwargs={"pk": sample_captive.pk})
    payload = {
        "name": "Updated Captive",
        "jurisdiction": "LUX",
        "formation_date": "2022-12-31",
        "minimum_capital": 750000,
        "paid_up_capital": 375000,
        "surplus": 75000,
    }
    response = api_client.put(url, payload, format="json")
    
    assert response.status_code == 200
    assert response.data["name"] == "Updated Captive"
    assert response.data["jurisdiction"] == "LUX"
    assert response.data["min_capital_surplus"] == 825000


def test_permission_authentication(api_client, sample_captive):
    """Test basic endpoints work without auth (consistent with spec)"""
    url = reverse("captive-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["count"] >= 0
