from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db import transaction
from .models import Project, LogSource, FileFilter, Schedule
from .forms import ProjectForm, LogSourceForm, FileFilterForm, ScheduleForm
from clients.models import Client


class ProjectListView(ListView):
    """List view for projects."""
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    ordering = ['name']
    
    def get_queryset(self):
        """Get projects with related data."""
        return Project.objects.select_related('client', 'created_by').prefetch_related('log_source', 'file_filter', 'schedule')
    
    def get_context_data(self, **kwargs):
        """Add search and filter functionality."""
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search')
        client_id = self.request.GET.get('client')
        
        queryset = context['projects']
        
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        
        context['projects'] = queryset
        context['clients'] = Client.objects.all()
        return context


class ProjectDetailView(DetailView):
    """Detail view for project."""
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        """Add related configuration data."""
        context = super().get_context_data(**kwargs)
        project = context['project']
        
        context['log_source'] = getattr(project, 'log_source', None)
        context['file_filter'] = getattr(project, 'file_filter', None)
        context['schedule'] = getattr(project, 'schedule', None)
        
        return context


class ProjectCreateView(CreateView):
    """Create new project."""
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')
    
    def form_valid(self, form):
        """Set the created_by field to current user."""
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Project "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class ProjectUpdateView(UpdateView):
    """Update existing project."""
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Project "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class ProjectDeleteView(DeleteView):
    """Delete project."""
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')
    
    def delete(self, request, *args, **kwargs):
        """Show success message after deletion."""
        project_name = self.get_object().name
        messages.success(request, f'Project "{project_name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Configuration views
def configure_log_source(request, project_id):
    """Configure log source for a project."""
    project = get_object_or_404(Project, id=project_id)
    log_source = getattr(project, 'log_source', None)
    
    if request.method == 'POST':
        form = LogSourceForm(request.POST, instance=log_source)
        if form.is_valid():
            log_source = form.save(commit=False)
            log_source.project = project
            log_source.save()
            messages.success(request, 'Log source configured successfully.')
            return redirect('project_detail', pk=project_id)
    else:
        form = LogSourceForm(instance=log_source)
    
    return render(request, 'projects/configure_log_source.html', {
        'form': form,
        'project': project
    })


def configure_file_filter(request, project_id):
    """Configure file filter for a project."""
    project = get_object_or_404(Project, id=project_id)
    file_filter = getattr(project, 'file_filter', None)
    
    if request.method == 'POST':
        form = FileFilterForm(request.POST, instance=file_filter)
        if form.is_valid():
            file_filter = form.save(commit=False)
            file_filter.project = project
            file_filter.save()
            messages.success(request, 'File filter configured successfully.')
            return redirect('project_detail', pk=project_id)
    else:
        form = FileFilterForm(instance=file_filter)
    
    return render(request, 'projects/configure_file_filter.html', {
        'form': form,
        'project': project
    })


def configure_schedule(request, project_id):
    """Configure schedule for a project."""
    project = get_object_or_404(Project, id=project_id)
    schedule = getattr(project, 'schedule', None)
    
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.project = project
            schedule.save()
            messages.success(request, 'Schedule configured successfully.')
            return redirect('project_detail', pk=project_id)
    else:
        form = ScheduleForm(instance=schedule)
    
    return render(request, 'projects/configure_schedule.html', {
        'form': form,
        'project': project
    })


def project_configuration(request, project_id):
    """Complete project configuration view."""
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        log_source_form = LogSourceForm(request.POST, instance=getattr(project, 'log_source', None))
        file_filter_form = FileFilterForm(request.POST, instance=getattr(project, 'file_filter', None))
        schedule_form = ScheduleForm(request.POST, instance=getattr(project, 'schedule', None))
        
        if log_source_form.is_valid() and file_filter_form.is_valid() and schedule_form.is_valid():
            with transaction.atomic():
                # Save log source
                log_source = log_source_form.save(commit=False)
                log_source.project = project
                log_source.save()
                
                # Save file filter
                file_filter = file_filter_form.save(commit=False)
                file_filter.project = project
                file_filter.save()
                
                # Save schedule
                schedule = schedule_form.save(commit=False)
                schedule.project = project
                schedule.save()
            
            messages.success(request, 'Project configuration saved successfully.')
            return redirect('project_detail', pk=project_id)
    else:
        log_source_form = LogSourceForm(instance=getattr(project, 'log_source', None))
        file_filter_form = FileFilterForm(instance=getattr(project, 'file_filter', None))
        schedule_form = ScheduleForm(instance=getattr(project, 'schedule', None))
    
    return render(request, 'projects/project_configuration.html', {
        'project': project,
        'log_source_form': log_source_form,
        'file_filter_form': file_filter_form,
        'schedule_form': schedule_form,
    })
