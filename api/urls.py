from django.urls import path

from .views import TopCustomersAPIView

urlpatterns = [
    path('top-clients/', TopCustomersAPIView.as_view()),
]