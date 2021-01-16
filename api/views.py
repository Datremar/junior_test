from rest_framework import generics

from api.serializers import CustomerSerializer
from gems.models import Customer


class TopCustomersAPIView(generics.ListAPIView):
    queryset = Customer.objects.all().order_by('spent_money').reverse()[:5]
    serializer_class = CustomerSerializer

