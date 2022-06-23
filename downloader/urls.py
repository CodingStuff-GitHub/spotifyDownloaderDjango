from . import views
from django.urls import path
urlpatterns = [
    path('', views.index, name='index'),
    path('download/<str:val>', views.download, name='download')
]
