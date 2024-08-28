
from django.urls import path
from .views import LoanProviderDashboardView, SignUpView, LoginView, CustomerDashboardView,BankPersonnelDashboardView

urlpatterns = [
   
    path('customer/dashboard/', CustomerDashboardView.as_view(), name='customer_dashboard'),
    path('loan-provider/dashboard/', LoanProviderDashboardView.as_view(), name='loan_provider_dashboard'),
    path('bank-personnel/dashboard/', BankPersonnelDashboardView.as_view(), name='bank_personnel_dashboard'),
]