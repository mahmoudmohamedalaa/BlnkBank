from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Loan, LoanFundApplication, FundPool, Transaction

class LoanProviderDashboardTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.loan_provider = User.objects.create_user(
            username='loan_provider',
            password='password123',
            role=User.Role.LoanProvider
        )
        self.fund_pool = FundPool.objects.create(total_amount=100000, available_amount=100000)
        self.loan_fund_application = LoanFundApplication.objects.create(
            provider=self.loan_provider,
            amount=50000,
            duration_months=12,
            interest_rate=5,
            status='Pending',
            fund_pool=self.fund_pool
        )

    def test_loan_provider_can_view_fund_applications(self):
        self.client.login(username='loan_provider', password='password123')
        response = self.client.get(reverse('loan_provider_dashboard'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        print(response.data)
        self.assertEqual(response.data[0]['provider'], self.loan_provider.id)
        
        
class LoanCustomerDashboardTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = User.objects.create_user(
            username='customer',
            password='password123',
            role=User.Role.Customer
        )
        self.fund_pool = FundPool.objects.create(total_amount=100000, available_amount=100000)
        self.loan = Loan.objects.create(
            customer=self.customer,
            amount=20000,
            interest_rate=5,
            duration=12,
            max_amount=30000,
            min_amount=10000,
            status='Approved',
            start_date='2023-01-01',
            end_date='2024-01-01',
            fund_pool=self.fund_pool,
            personnel=None  # Add a BankPersonnel user if needed
        )

    def test_customer_can_view_loans(self):
        self.client.login(username='customer', password='password123')
        response = self.client.get(reverse('customer_dashboard'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['customer'], self.customer.id)

    def test_customer_can_make_payment(self):
        self.client.login(username='customer', password='password123')
        payment_data = {
            'loan_id': self.loan.loan_id,  # Use loan_id here instead of id
            'amount': 1000,
            'transaction_date': '2023-08-01'
        }
        response = self.client.post(reverse('customer_dashboard'), payment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.first().amount, 1000)
        
        
        
class BankPersonnelDashboardTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.bank_personnel = User.objects.create_user(
            username='bank_personnel',
            password='password123',
            role=User.Role.BankPersonnel
        )
        self.loan_provider = User.objects.create_user(
            username='loan_provider',
            password='password123',
            email='aa@gmail.com',
            role=User.Role.LoanProvider
        )
        self.customer = User.objects.create_user(
            username='customer',
            password='password123',
            email='aa2@gmail.com',
            role=User.Role.Customer
        )
        self.fund_pool = FundPool.objects.create(total_amount=100000, available_amount=100000)
        self.loan_fund_application = LoanFundApplication.objects.create(
            provider=self.loan_provider,
            amount=50000,
            duration_months=12,
            interest_rate=5,
            status='Pending',
            fund_pool=self.fund_pool
        )
        self.loan = Loan.objects.create(
            customer=self.customer,
            amount=20000,
            interest_rate=5,
            duration=12,
            max_amount=30000,
            min_amount=10000,
            status='Pending',
            start_date='2023-01-01',
            end_date='2024-01-01',
            fund_pool=self.fund_pool,
            personnel=self.bank_personnel
        )

    def test_bank_personnel_can_view_all_applications(self):
        self.client.login(username='bank_personnel', password='password123')
        response = self.client.get(reverse('bank_personnel_dashboard'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['loan_fund_applications']), 1)
        self.assertEqual(len(response.data['loans']), 1)
