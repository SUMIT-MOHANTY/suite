from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Invoice, Statement
from .serializers import InvoiceSerializer, StatementSerializer
from .services import StatementService

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        captive_id = self.request.query_params.get('captive_id')
        status_filter = self.request.query_params.get('status')
        
        if captive_id:
            queryset = queryset.filter(captive_id=captive_id)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset.select_related('policy', 'captive')

class StatementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Statement.objects.all()
    serializer_class = StatementSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        captive_id = self.request.query_params.get('captive_id')
        year = self.request.query_params.get('year')
        
        if captive_id:
            queryset = queryset.filter(captive_id=captive_id)
        if year:
            queryset = queryset.filter(year=year)
            
        return queryset.select_related('captive')
    
    @action(detail=False, methods=['post'])
    def generate_annual(self, request):
        """Generate annual statements for a captive"""
        captive_id = request.data.get('captive_id')
        year = request.data.get('year')
        
        if not captive_id or not year:
            return Response(
                {'error': 'captive_id and year are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        statements = StatementService.generate_annual_statement(
            int(captive_id),
            int(year)
        )
        serializer = self.get_serializer(statements, many=True)
        return Response(serializer.data)
