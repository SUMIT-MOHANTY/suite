from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Claim, ClaimTimeline
from .serializers import ClaimSerializer

class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        with transaction.atomic():
            old_status = self.get_object().status
            claim = serializer.save()
            if old_status != claim.status:
                ClaimTimeline.objects.create(
                    claim=claim,
                    event_type='status_change',
                    description=f'Status changed from {old_status} to {claim.status}',
                    performed_by=self.request.user
                )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == 'intake':
            context['is_intake'] = True
        return context

    @action(detail=False, methods=['post'])
    def intake(self, request):
        """Create new claim with timeline entry"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        claim = serializer.save()
        ClaimTimeline.objects.create(
            claim=claim,
            event_type='intake',
            description='Claim submitted via intake form',
            performed_by=request.user
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def bulk_status_update(self, request):
        """Mass update claim statuses"""
        ids = request.data.get('ids', [])
        new_status = request.data.get('status')
        if not ids or not new_status:
            return Response({'error': 'ids and status required'}, status=status.HTTP_400_BAD_REQUEST)
        updated = Claim.objects.filter(id__in=ids).update(status=new_status)
        return Response({'updated': updated})

    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        claim = self.get_object()
        timeline = claim.timeline_events.all()
        serializer = self.get_serializer(timeline, many=True)
        return Response(serializer.data)
