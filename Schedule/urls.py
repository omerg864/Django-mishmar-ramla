from django.contrib import admin
from django.urls import path
from . import views
from .views import OrganizationDetailView, ShifttableView
from .views import ServedSumListView, ServedSumShiftDetailView, ServedSumReinforcementsDetailView
from .views import OrganizationSuggestionView, OrganizationCreateView, OrganizationListView
from .views import organization_update
from .views import ArmingDayView, ArmingMonthView, ArmingLogUpdate, ArmingCreateView, Validation_Log_Signature, ArmingRequestView, ArmingRequestDetailView, ArmingRequestListView

urlpatterns = [
    path("", views.home, name="Schedule-Home"),
    path("serve/", views.shift_view, name="Schedule-Serve"),
    path("organization/", OrganizationListView.as_view(), name="Schedule-Organization"),
    path("serve/sum", ServedSumListView.as_view(), name="Schedule-Served-sum"),
    path("settings/", views.settings_view, name="Schedule-Settings"),
    path("organization/<int:pk>/update", organization_update, name="organization-update"),
    path("shift/<int:pk>/update", views.shift_update_view, name="shift-update"),
    path('organization/<int:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('serve/sum/shift/<int:pk>/', ServedSumShiftDetailView.as_view(), name='served-sum-shift'),
    path('serve/sum/reinforcement/<int:pk>/', ServedSumReinforcementsDetailView.as_view(), name='served-sum-reinforcement'),
    path('organization/table/shift/<int:pk>/', ShifttableView.as_view(), name='organization-table-shift'),
    path("organization/<int:pk>/suggestion", OrganizationSuggestionView.as_view(), name="organization-suggestion"),
    path("organization/new", OrganizationCreateView.as_view(), name="organization-new"),
    path('<int:year>/<str:month>/<int:day>/', ArmingDayView.as_view(), name="armingday"),
    path('<int:year>/<str:month>/',  ArmingMonthView.as_view(), name="armingmonth"),
    path('signature/<int:pk>/',  ArmingLogUpdate.as_view(), name="signature"),
    path('ArmingLog/new/',  ArmingCreateView.as_view(), name="arming-new"),
    path('validation/signature', Validation_Log_Signature, name="validation-signature"),
    path('arminglog/changerequest/new', ArmingRequestView.as_view(), name="arming-changerequest"),
    path('arminglog/request/<int:pk>/', ArmingRequestDetailView.as_view(), name="arming-request"),
    path('arminglog/requests/', ArmingRequestListView.as_view(), name="arming-requests-list"),
]
