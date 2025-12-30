from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/api/stats/', views.admin_stats_api, name='admin_stats_api'),
    path('pricing/', views.pricing, name='pricing'),
    path('academy/', views.academy, name='academy'),
    path('about/', views.about, name='about'),
    path('support/', views.support, name='support'),
    
    # Export endpoints
    path('export/trades/', views.export_trades, name='export_trades'),
    path('admin/export/users/', views.export_users, name='export_users'),
    path('admin/export/trades/', views.export_all_trades, name='export_all_trades'),
    
    # Admin actions
    path('admin/send-notification/', views.send_notification_view, name='send_notification'),
    path('admin/generate-report/', views.generate_report_view, name='generate_report'),
]
