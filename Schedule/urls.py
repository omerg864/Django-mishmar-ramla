from django.contrib import admin
from django.urls import path
from . import views
from .views import OrganizationUpdateView, ShiftUpdateView, OrganizationDetailView, ShifttableView
from .views import ServedSumListView, ServedSumShiftDetailView, ServedSumReinforcementsDetailView

urlpatterns = [
    path("", views.home, name="Schedule-Home"),
    path("serve/", views.shift_view, name="Schedule-Serve"),
    path("organization/", views.organization, name="Schedule-Organization"),
    path("serve/sum", ServedSumListView.as_view(), name="Schedule-Served-sum"),
    path("suggestion/", views.suggestion, name="Schedule-Suggestion"),
    path("settings/", views.settings_view, name="Schedule-Settings"),
    path("organization/<int:pk>/update", OrganizationUpdateView.as_view(), name="organization-update"),
    path("shift/<int:pk>/update", ShiftUpdateView.as_view(), name="shift-update"),
    path('organization/<int:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('serve/sum/shift/<int:pk>/', ServedSumShiftDetailView.as_view(), name='served-sum-shift'),
    path('serve/sum/reinforcement/<int:pk>/', ServedSumReinforcementsDetailView.as_view(), name='served-sum-reinforcement'),
    path('organization/table/shift/<int:pk>/', ShifttableView.as_view(), name='organization-table-shift'),
]
