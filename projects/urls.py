from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    
    # Configuration URLs
    path('<int:project_id>/configure/', views.project_configuration, name='project_configuration'),
    path('<int:project_id>/configure/log-source/', views.configure_log_source, name='configure_log_source'),
    path('<int:project_id>/configure/file-filter/', views.configure_file_filter, name='configure_file_filter'),
    path('<int:project_id>/configure/schedule/', views.configure_schedule, name='configure_schedule'),
]
