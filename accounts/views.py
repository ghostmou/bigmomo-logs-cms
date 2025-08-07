from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.crypto import get_random_string
from django.db import transaction
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm, UserProfileForm


def is_admin(user):
    """Check if user is admin."""
    return user.is_authenticated and user.is_admin


class CustomLoginView(LoginView):
    """Custom login view with role-based redirect."""
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        """Check if user is active and redirect appropriately."""
        user = form.get_user()
        if user.is_blocked:
            messages.error(self.request, 'Your account has been blocked. Please contact an administrator.')
            return self.form_invalid(form)
        
        if user.is_pending:
            messages.error(self.request, 'Your account is pending approval. Please contact an administrator.')
            return self.form_invalid(form)
        
        # Check if password needs to be changed
        if not user.is_password_changed:
            messages.warning(self.request, 'Please change your password on first login.')
            return super().form_valid(form)
        
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect based on user role."""
        if not self.request.user.is_password_changed:
            return reverse_lazy('password_change')
        return reverse_lazy('dashboard')


@login_required
def dashboard(request):
    """Dashboard view for authenticated users."""
    context = {
        'user': request.user,
        'clients_count': request.user.created_clients.count(),
        'projects_count': request.user.created_projects.count(),
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    """User profile view."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})


class CustomPasswordChangeView(PasswordChangeView):
    """Custom password change view."""
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        """Mark password as changed after successful change."""
        response = super().form_valid(form)
        self.request.user.is_password_changed = True
        self.request.user.save()
        messages.success(self.request, 'Password changed successfully.')
        return response


# Admin-only views
class UserListView(ListView):
    """List view for all users (admin only)."""
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    ordering = ['-date_joined']
    
    def get_queryset(self):
        """Filter users based on search."""
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                username__icontains=search
            ) | queryset.filter(
                email__icontains=search
            ) | queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            )
        return queryset


class UserCreateView(CreateView):
    """Create new user (admin only)."""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')
    
    def form_valid(self, form):
        """Generate random password and save user."""
        with transaction.atomic():
            # Generate random password
            random_password = get_random_string(12)
            user = form.save(commit=False)
            user.set_password(random_password)
            user.is_password_changed = False
            user.save()
            
            messages.success(
                self.request, 
                f'User {user.username} created successfully. Temporary password: {random_password}'
            )
        
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    """Update user (admin only)."""
    model = User
    form_class = CustomUserChangeForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')
    
    def form_valid(self, form):
        """Prevent admin from blocking themselves."""
        user = form.instance
        if user == self.request.user and user.is_blocked:
            messages.error(self.request, 'You cannot block your own account.')
            return self.form_invalid(form)
        
        messages.success(self.request, f'User {user.username} updated successfully.')
        return super().form_valid(form)


def reset_user_password(request, pk):
    """Reset user password (admin only)."""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        random_password = get_random_string(12)
        user.set_password(random_password)
        user.is_password_changed = False
        user.save()
        
        messages.success(
            request, 
            f'Password for {user.username} has been reset. New password: {random_password}'
        )
        return redirect('user_list')
    
    return render(request, 'accounts/reset_password_confirm.html', {'user': user})


def toggle_user_status(request, pk):
    """Toggle user blocked status (admin only)."""
    user = get_object_or_404(User, pk=pk)
    
    if user == request.user:
        messages.error(request, 'You cannot block your own account.')
        return redirect('user_list')
    
    if user.is_blocked:
        user.status = User.UserStatus.ACTIVE
        messages.success(request, f'User {user.username} has been unblocked.')
    else:
        user.status = User.UserStatus.BLOCKED
        messages.success(request, f'User {user.username} has been blocked.')
    
    user.save()
    return redirect('user_list')
