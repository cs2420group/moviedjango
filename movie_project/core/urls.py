from django.contrib import admin
from django.urls import path
from reviews import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'), 
    path('api/items/<int:pk>/', views.item_api_detail),            
]


