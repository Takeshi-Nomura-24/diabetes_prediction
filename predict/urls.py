# predict/urls.py の例
from django.urls import path
from . import views

app_name = 'predict'  # これがないと views.py 内の URL 指定が動きません

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict, name='predict'),
    path('view_data/', views.view_data, name='view_data'),
    path('exportcsv/', views.exportcsv, name='exportcsv'),
    path('view_pima_indian/', views.view_pima_indian, name='view_pima_indian'),
]
