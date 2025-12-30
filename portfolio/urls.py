from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio_dashboard, name='portfolio_dashboard'),
    path('settings/', views.update_portfolio, name='update_portfolio'),
    path('transaction/add/', views.add_transaction, name='add_transaction'),
]
