from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count
from .models import Client
from .forms import ClientForm


class ClientListView(ListView):
    """List view for clients."""
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'
    ordering = ['name']
    
    def get_queryset(self):
        """Get clients with project count."""
        return Client.objects.annotate(project_count=Count('projects'))
    
    def get_context_data(self, **kwargs):
        """Add search functionality."""
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search')
        if search:
            context['clients'] = context['clients'].filter(name__icontains=search)
        return context


class ClientCreateView(CreateView):
    """Create new client."""
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('client_list')
    
    def form_valid(self, form):
        """Set the created_by field to current user."""
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Client "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    """Update existing client."""
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('client_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Client "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class ClientDeleteView(DeleteView):
    """Delete client."""
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')
    
    def delete(self, request, *args, **kwargs):
        """Show success message after deletion."""
        client_name = self.get_object().name
        messages.success(request, f'Client "{client_name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)
