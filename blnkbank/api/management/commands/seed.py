from django.core.management.base import BaseCommand
from api.models import User, Loan, LoanFundApplication, FundPool
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # Create a FundPool
        fund_pool = FundPool.objects.create(total_amount=500000, available_amount=500000)

        # Create Loan Providers
        loan_provider_1 = User.objects.create_user(
            username='loanprovider12455',
            password='password123',
            email='bbb1@gmail.com',
            role=User.Role.LoanProvider
        )
        loan_provider_2 = User.objects.create_user(
            username='loanprovider2233',
            password='password123',
            email='cccc123@gmail.com',
            role=User.Role.LoanProvider
        )

        # Create Customers
        customer_1 = User.objects.create_user(
            username='customer12',
            password='password123',
            email='eee@e.com',
            role=User.Role.Customer
        )
        customer_2 = User.objects.create_user(
            username='customer22',
            password='password123',
            email='fff@f.com',
            role=User.Role.Customer
        )

        # Create Loan Fund Applications
        LoanFundApplication.objects.create(
            provider=loan_provider_1,
            amount=100000,
            duration_months=12,
            interest_rate=5,
            status='Approved',
            fund_pool=fund_pool,
            application_date=timezone.now()
        )

        LoanFundApplication.objects.create(
            provider=loan_provider_2,
            amount=150000,
            duration_months=24,
            interest_rate=4.5,
            status='Pending',
            fund_pool=fund_pool,
            application_date=timezone.now()
        )

        # Create Loans
        Loan.objects.create(
            customer=customer_1,
            amount=50000,
            interest_rate=5,
            duration=12,
            max_amount=100000,
            min_amount=10000,
            status='Approved',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=365),
            fund_pool=fund_pool
        )

        Loan.objects.create(
            customer=customer_2,
            amount=75000,
            interest_rate=4.5,
            duration=24,
            max_amount=150000,
            min_amount=20000,
            status='Pending',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=730),
            fund_pool=fund_pool
        )

        self.stdout.write("Database seeded successfully.")
