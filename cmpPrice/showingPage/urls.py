from django.urls import path
from . import views

app_name = 'showingPage'
urlpatterns = [
    path('',views.home,name='home'),
    path('/cmpprice/<str:id>/',views.cmpPrice,name='cmpPrice'),
    ]