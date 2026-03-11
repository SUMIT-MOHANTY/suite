from rest_framework import serializers
from .models import CaptiveModel


class PolicyCountSerializer(serializers.Serializer):
    """Writable nested serializer for policy count badge return (used only in list serializer)"""
    policy_count = serializers.IntegerField(read_only=True)


class CaptiveSerializer(serializers.ModelSerializer):
    """Main serializer for Captive CRUD operations"""
    
    min_capital_surplus = serializers.IntegerField(read_only=True)
    policy_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = CaptiveModel
        fields = [
            'id',
            'name',
            'jurisdiction',
            'formation_date',
            'minimum_capital',
            'paid_up_capital',
            'surplus',
            'status',
            'min_capital_surplus',
            'policy_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'min_capital_surplus', 'policy_count', 'created_at', 'updated_at']
    
    def get_policy_count(self, obj):
        """Return policy count for badge display"""
        return obj.policy_count
    
    def validate(self, attrs):
        """Validate the entire payload"""
        minimum_capital = attrs.get('minimum_capital', 0)
        paid_up_capital = attrs.get('paid_up_capital', 0)
        
        if paid_up_capital > minimum_capital:
            raise serializers.ValidationError(
                {"paid_up_capital": "paid_up_capital must not exceed minimum_capital"}
            )
        
        return attrs


class CaptiveListSerializer(CaptiveSerializer):
    """Special list serializer to enable policy_count badge"""
    policy_count = PolicyCountSerializer(source='*', read_only=True)
    
    class Meta(CaptiveSerializer.Meta):
        pass
