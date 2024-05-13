from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Issue, Status

class IssueListView(LoginRequiredMixin, ListView):
    template_name = 'issues/list.html'
    model = Issue
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published_status = Status.objects.get(name="published")
        context["issue_list"] = (
            Issue.objects.filter(status=published_status)
            .order_by("created_on")
            .reverse()
        )
        return context

class IssueDetailView(LoginRequiredMixin, DetailView):
    template_name = 'issues/detail.html'
    model = Issue

class IssueCreateView(LoginRequiredMixin, CreateView):
    template_name = 'issues/issue_create.html'
    model = Issue
    fields = ['title', 'description', 'status', 'assigned_to']  # Define fields here
    success_url = reverse_lazy('list') 

    def form_valid(self, form):
        form.instance.reporter = self.request.user  
        return super().form_valid(form)  

class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'issues/update.html'
    model = Issue
    fields = ['title', 'description', 'status', 'assigned_to']  # Define fields here
    success_url = reverse_lazy('list')  

    def test_func(self):
        issue = self.get_object()
        return issue.reporter == self.request.user 
