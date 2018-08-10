from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from plans import views

urlpatterns = [
    path('plans/', views.CarrierPlanList.as_view(), name='plans-list'),
    path('plans/<int:pk>/', views.CarrierPlanDetail.as_view(), name='plans-detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
