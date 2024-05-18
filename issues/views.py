from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Issue, Status

class IssueListView(LoginRequiredMixin, ListView):
    template_name = 'issues/board.html'
    model = Issue
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        to_do = Status.objects.get(name="to do")
        in_progress = Status.objects.get(name="in progress")
        done = Status.objects.get(name="done")
        context["to_do_list"] = Issue.objects.filter(
            status=to_do
        ).order_by("created_on")
        context["in_progress_list"] = Issue.objects.filter(
            status=in_progress
        ).order_by("created_on")
        context["done_list"] = Issue.objects.filter(
            status=done
        ).order_by("created_on")
        return context

class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'issues/edit.html'
    model = Issue
    fields = ["status"]  
    success_url = reverse_lazy('board')  

    def test_func(self):
        issue = self.get_object()
        return issue.reporter == self.request.user
