from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Authentication
    path('', views.dashboard, name='dashboard'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    
    # User profile
    path('profile/', views.profile, name='profile'),
    
    # Admin user management
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/reset-password/', views.reset_user_password, name='user_reset_password'),
    path('users/<int:pk>/toggle-status/', views.toggle_user_status, name='user_toggle_status'),
]
