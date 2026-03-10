from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from apps.auth.permissions import IsBroker  # stub: raise 403 for non-broker role
import hashlib

from .models import Policy
from .serializers import PolicySerializer, ACORDExcelSerializer

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get("status")
        captive_id = self.request.query_params.get("captive_id")
        if status:
            qs = qs.filter(status=status)
        if captive_id:
            qs = qs.filter(captive_id=captive_id)
        return qs

    @action(detail=True, methods=['post'])
    def renew(self, request, pk=None):
        instance = self.get_object()
        effective_date = request.data.get("effective_date")
        if not effective_date:
            return Response({"error": {"message": "effective_date required"}}, status=400)
        new_policy = Policy.objects.create(
            captive_id=instance.captive_id,
            policy_number=f"{instance.policy_number}-R",
            effective_date=effective_date,
            expiry_date=None,  # calculate later
            premium=instance.premium,
            status='quote'
        )
        return Response(PolicySerializer(new_policy).data, status=201)

    @action(detail=True, methods=['post'])
    def endorse(self, request, pk=None):
        instance = self.get_object()
        try:
            new_premium = request.data.get("new_premium", instance.premium)
            instance.premium = new_premium
            instance.save()
            instance.change_status("endorsed")
            return Response(PolicySerializer(instance).data)
        except ValidationError as e:
            return Response({"error": {"message": str(e)}}, status=400)

    @action(detail=True, methods=['get'])
    def export(self, request, pk=None):
        instance = self.get_object()
        excel_ser = ACORDExcelSerializer()
        buf = excel_ser.generate_xlsx(instance)
        content = buf.read()
        sha256 = hashlib.sha256(content).hexdigest()
        response = Response(content, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="policy_{instance.policy_number}.xlsx"'
        response['X-SHA256'] = sha256
        return response
