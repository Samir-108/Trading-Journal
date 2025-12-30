from django.urls import path
from . import views

urlpatterns = [
    path('', views.trade_list, name='trade_list'),
    path('add/', views.trade_create, name='trade_create'),
    path('<int:pk>/', views.trade_detail, name='trade_detail'),
    path('<int:pk>/edit/', views.trade_update, name='trade_update'),
    path('<int:pk>/delete/', views.trade_delete, name='trade_delete'),
    
    path('strategies/', views.strategy_list, name='strategy_list'),
    path('strategies/add/', views.strategy_create, name='strategy_create'),
]
