from django.urls import path
from .views import IssueListView, IssueUpdateView

urlpatterns = [
    path('board/', IssueListView.as_view(), name='board'),
    path('issue/<int:pk>/edit/', IssueUpdateView.as_view(), name='edit_issue'),
]
