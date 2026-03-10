from rest_framework import serializers
from .models import Claim, ClaimTimeline

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class ClaimTimelineSerializer(serializers.ModelSerializer):
    performed_by_name = serializers.CharField(source='performed_by.username', read_only=True)
    
    class Meta:
        model = ClaimTimeline
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['createdAt'] = data.pop('created_at')
        data.pop('createdAt', None)
        return data
