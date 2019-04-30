from django.urls import path
from basic_app import views

app_name = 'app'

urlpatterns = [
    path('',views.page_one,name='page_one'),
    path('user_login/',views.user_login,name='user_login'),
    path('register/',views.register,name='register'),
    path('user_details/',views.user_details,name='user_details'),
    path('groundwaterlevel/',views.groundwaterlevel,name='groundwaterlevel'),
    path('ajax/load-sites/', views.load_sites, name='ajax_load_sites'),
    path('ajax/forecast/', views.model, name='ajax_forecast'),
    path('weatherforecast/',views.weatherforecast,name='weatherforecast'),
    path('addbookmark/<c>/',views.addbookmark,name='addbookmark'),
    path('deletebookmark/<c>/',views.deletebookmark,name='deletebookmark'),
]