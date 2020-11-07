from django.urls import path, re_path
from . import views
from .views import DealsView, UploadDealsView # api_overview , upload_page, show_data, post_data

urlpatterns = [
    path('deal-view/', DealsView.as_view(), name='deal-view'),
    path('deal-upload/', UploadDealsView.as_view(), name='deal-upload'),
    # path('', api_overview, name="api-overview"),
    # path('upload-data/', upload_page, name='upload-data'),
    # path('post-data/', post_data, name='post-data'),
    # path('get-data/', show_data, name='get-data'),
]