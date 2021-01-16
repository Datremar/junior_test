from django.urls import path

from gems.views import HomePageView, UploadDataView, DataView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('upload/', UploadDataView.as_view(), name='upload'),
    path('data-view/', DataView.as_view(), name='data'),
]