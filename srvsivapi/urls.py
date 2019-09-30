from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('addemployee', views.addEmployee),
    path('getEmployees',views.getEmployees),
    path('createSRV',views.createSRV),
    path('createSIV',views.createSIV),
    path('createsrvsiv',views.createsrvsiv),
    path('getsrvs', views.getsrvs)
]