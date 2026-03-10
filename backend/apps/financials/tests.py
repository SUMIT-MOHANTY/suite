from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from decimal import Decimal
import pytest
from unittest.mock import patch
from io import StringIO
import logging

from .serializers import InvoiceSerializer
from .models import Invoice, Statement
from apps.captives.models import Captive
from apps.policies.models import Policy

User = get_user_model()

class InvoiceTests(TestCase):
    def test_earn_premium_rounding_rounds_up_to_pennies(self):
        amount = Decimal('100.567')
        serializer = InvoiceSerializer()
        
        # Mock policy
        class MockPolicy:
            effective_date = '2023-01-01'
            expiry_date = '2023-12-31'
            premium = 1000
        
        result = serializer.earn_premium_calc(
            amount, MockPolicy(), '2023-01-01', '2023-01-31'
        )
        assert result == Decimal('8.47')  # Correct rounding
    
    @patch('logging.Logger.info')
    def test_qb_skipped_in_sandbox_true_logs_in_memory(self, mock_log):
        from .qb_stub import QBClient
        
        # Capture log output
        log_capture = StringIO()
        handler = logging.StreamHandler(log_capture)
        logger = logging.getLogger('apps.financials.qb_stub')
        logger.addHandler(handler)
        
        client = QBClient('fake_token', sandbox=True)
        client.create_invoice(None)
        
        logs = log_capture.getvalue()
        assert 'QB sync disabled' in logs or 'QB sync not enabled' in logs
