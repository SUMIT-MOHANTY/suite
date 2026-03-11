from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from models import Captive, Contact
from serializers import CaptiveSerializer, ContactSerializer
class CaptiveViewSet(viewsets.ModelViewSet):
    queryset = Captive.objects.all()
    serializer_class = CaptiveSerializer
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=201)
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    @action(detail=True, methods=['get'])
    def contacts(self, request, pk=None):
        captive = Contact.objects.filter(captive_id=pk)
        serializer = self.get_serializer(captive, many=True)
        return Response(serializer.data)
class CaptiveListView(ListView):
    model = Captive
    template_name = 'list.html'
    paginate_by = 20
    context_object_name = 'page_obj'
class CaptiveDetailView(DetailView):
    model = Captive
    template_name = 'detail.html'
    context_object_name = 'captive'
