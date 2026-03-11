from rest_framework import serializers
from models import Captive, Contact
class CaptiveSerializer(serializers.ModelSerializer):
    min_capital_surplus = serializers.ReadOnlyField()
    class Meta:
        model = Captive
        fields = ['id', 'name', 'jurisdiction', 'formation_date', 'minimum_capital',
                  'paid_up_capital', 'surplus', 'min_capital_surplus', 'created_at', 'updated_at']
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'captive', 'name', 'email', 'role', 'phone', 'created_at']
