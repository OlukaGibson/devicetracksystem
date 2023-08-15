from django.urls import path
from . import views

urlpatterns = [
    path('', views.fetch_and_store_thingspeak_data, name='fetch_and_store_data'),
    path('show_latest_data/', views.show_latest_data_on_map, name='show_latest_data'),
]
#fetch_and_store_data/