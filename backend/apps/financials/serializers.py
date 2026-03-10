from rest_framework import serializers
from .models import Invoice, Statement
from django.db import transaction
import decimal

class InvoiceSerializer(serializers.ModelSerializer):
    policy = serializers.SerializerMethodField()
    captive = serializers.SerializerMethodField()
    balance_forward = serializers.SerializerMethodField()
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'policy', 'captive', 'due_date', 'invoice_number',
            'lines', 'status', 'issued_at', 'paid_at', 'balance_forward',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['invoice_number', 'balance_forward']
    
    def get_policy(self, obj):
        from apps.policies.serializers import PolicySerializer
        return PolicySerializer(obj.policy).data
    
    def get_captive(self, obj):
        from apps.captives.serializers import CaptiveSerializer
        return CaptiveSerializer(obj.captive).data
    
    def get_balance_forward(self, obj):
        from .services import InvoiceService
        return InvoiceService.get_balance_forward(obj.policy_id)
    
    @transaction.atomic
    def create(self, validated_data):
        captive = validated_data['captive']
        
        # Generate invoice number
        last_num = captive.invoices.filter(
            invoice_number__startswith=f"INV{captive.short_code}"
        ).count()
        sequence = str(last_num + 1).zfill(4)
        validated_data['invoice_number'] = f"INV{captive.short_code}{sequence}"
        
        # Calculate earned premium
        policy = validated_data['policy']
        from_date = validated_data.get('from_date', policy.effective_date)
        to_date = validated_data.get('to_date', policy.expiry_date)
        amount = self.earn_premium_calc(
            policy.premium,
            policy,
            from_date,
            to_date
        )
        
        validated_data['lines'] = [{
            'type': 'earned_premium',
            'amount': str(amount),
            'vat': '0.00'
        }]
        
        return super().create(validated_data)
    
    @staticmethod
    def earn_premium_calc(amount, policy, from_date, to_date):
        """Calculate earned premium rounded to 2 decimals"""
        days_total = (policy.expiry_date - policy.effective_date).days
        days_earned = (to_date - from_date).days
        
        if days_total <= 0:
            return decimal.Decimal('0.00')
        
        earned = (decimal.Decimal(str(amount)) * days_earned) / days_total
        return earned.quantize(decimal.Decimal('0.01'))

class StatementSerializer(serializers.ModelSerializer):
    captive = serializers.SerializerMethodField()
    
    class Meta:
        model = Statement
        fields = [
            'id', 'captive', 'year', 'month', 'generated_at',
            'lines', 'created_at', 'updated_at'
        ]
    
    def get_captive(self, obj):
        from apps.captives.serializers import CaptiveSerializer
        return CaptiveSerializer(obj.captive).data
