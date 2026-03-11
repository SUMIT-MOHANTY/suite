from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view
from django.db.models import Count
from .models import CaptiveModel
from .serializers import CaptiveSerializer, CaptiveListSerializer

@extend_schema_view(
    list=extend_schema(
        description="List all captives with pagination",
        parameters=[
            {
                'name': 'page',
                'in': 'query',
                'type': 'integer',
                'description': 'Page number for pagination',
                'required': False
            }
        ],
        responses={200: CaptiveListSerializer(many=True)}
    ),
    create=extend_schema(
        description="Create a new captive",
        examples=[
            OpenApiExample(
                "CreateExample",
                value={
                    "name": "ABay Insurance Co.",
                    "jurisdiction": "AVG",
                    "formation_date": "2024-01-15",
                    "minimum_capital": 500000,
                    "paid_up_capital": 250000,
                    "surplus": 50000,
                },
                request_only=True,
            )
        ],
    ),
    retrieve=extend_schema(
        description="Get a specific captive by ID"
    ),
    update=extend_schema(
        description="Update an existing captive",
        examples=[
            OpenApiExample(
                "UpdateExample",
                value={
                    "minimum_capital": 600000,
                    "surplus": 60000,
                },
                request_only=True,
            )
        ],
    ),
    partial_update=extend_schema(
        description="Partially update an existing captive"
    ),
    destroy=extend_schema(
        description="Delete a captive"
    ),
)
class CaptiveViewSet(viewsets.ModelViewSet):
    """Captive management CRUD operations"""
    queryset = CaptiveModel.objects.all()

    def get_queryset(self):
        """Annotate queryset with policy count for list view"""
        if self.action == 'list':
            return self.queryset.annotate(
                _policy_count=Count('policies')  # Assuming related_name='policies'
            )
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return CaptiveListSerializer
        return CaptiveSerializer

    def perform_create(self, serializer):
        """Override to set created_by"""
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)

    def perform_update(self, serializer):
        """Override to set updated_by"""
        serializer.save(updated_by=self.request.user if self.request.user.is_authenticated else None)
