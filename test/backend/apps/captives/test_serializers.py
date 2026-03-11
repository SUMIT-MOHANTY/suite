import pytest
from rest_framework.exceptions import ValidationError
from backend.apps.captives.models import CaptiveModel
from backend.apps.captives.serializers import CaptiveSerializer


@pytest.fixture
def valid_payload():
    """Valid payload for testing"""
    return {
        "name": "Test Captive Ltd.",
        "jurisdiction": "AVG",
        "formation_date": "2024-02-01",
        "minimum_capital": 100000,
        "paid_up_capital": 50000,
        "surplus": 20000,
    }


@pytest.fixture
def existent_captive(db):
    """Existent captive instance"""
    return CaptiveModel.objects.create(
        name="Existent Captive",
        jurisdiction="BVD",
        formation_date="2023-01-01",
        minimum_capital=500000,
        paid_up_capital=250000,
        surplus=50000,
    )


def test_create_with_valid_data(valid_payload):
    """Test creating captive with valid data"""
    serializer = CaptiveSerializer(data=valid_payload)
    assert serializer.is_valid()
    captive = serializer.save()
    assert captive.min_capital_surplus == 120000


def test_constraint_validation(valid_payload):
    """Test validation when paid_up_capital > minimum_capital"""
    valid_payload["paid_up_capital"] = 150000
    serializer = CaptiveSerializer(data=valid_payload)
    assert not serializer.is_valid()
    assert "paid_up_capital" in serializer.errors
    assert "must not exceed" in str(serializer.errors)


def test_derived_fields_calculation(valid_payload):
    """Test that min_capital_surplus is calculated correctly"""
    serializer = CaptiveSerializer(data=valid_payload)
    assert serializer.is_valid()
    captive = serializer.save()
    assert captive.min_capital_surplus == valid_payload["minimum_capital"] + valid_payload["surplus"]


def test_update_existing_captive(existent_captive):
    """Test updating existing captive with valid data"""
    payload = {
        "minimum_capital": 600000,
        "surplus": 100000,
    }
    serializer = CaptiveSerializer(existent_captive, data=payload, partial=True)
    assert serializer.is_valid()
    updated = serializer.save()
    assert updated.min_capital_surplus == 700000


def test_unique_name_jurisdiction_constraint(existent_captive, valid_payload):
    """Test unique name+jurisdiction constraint"""
    valid_payload["name"] = "Existent Captive"
    valid_payload["jurisdiction"] = "BVD"  # Same as existent
    serializer = CaptiveSerializer(data=valid_payload)
    assert not serializer.is_valid()
    assert "name" in str(serializer.errors) or "unique" in str(serializer.errors).lower()
