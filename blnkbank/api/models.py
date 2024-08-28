from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver



class User(AbstractUser):
    class Role (models.TextChoices):
        Customer= 'CUSTOMER', 'Customer'
        LoanProvider= 'LOANPROVIDER', 'Loan Provider'
        BankPersonnel='BANKPERSONNEL', 'Bank Personnel'
        
    
    base_role=Role.BankPersonnel
    role=models.CharField(max_length=50, choices=Role.choices,default=base_role)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    def save(self, *args, **kwargs):
        if not self.pk and not self.role:
           self.role=self.base_role
        return super().save(*args, **kwargs)
       
       
       
class BankManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.BankPersonnel)


class BankPersonnel(User):

    base_role = User.Role.BankPersonnel
    objects = BankManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Bank Personnel"





class BankerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    banker_id = models.IntegerField(null=True, blank=True)






class LoanProviderManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.LoanProvider)


class LoanProvider(User):

    base_role = User.Role.LoanProvider

    objects = LoanProviderManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Loan Providers"


class LoanProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    LoanProvider_id = models.IntegerField(null=True, blank=True)



    





class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.Customer)




class Customer(User):
    base_role = User.Role.Customer
    objects = CustomerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Customers"
    



class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.IntegerField(null=True, blank=True)
    credit_score = models.IntegerField(default=0)




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.Role.Customer:
            CustomerProfile.objects.create(user=instance)
        elif instance.role == User.Role.LoanProvider:
            LoanProviderProfile.objects.create(user=instance)
        elif instance.role == User.Role.BankPersonnel:
            BankerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == User.Role.Customer and hasattr(instance, 'customerprofile'):
        instance.customerprofile.save()
    elif instance.role == User.Role.LoanProvider and hasattr(instance, 'loanproviderprofile'):
        instance.loanproviderprofile.save()
    elif instance.role == User.Role.BankPersonnel and hasattr(instance, 'bankerprofile'):
        instance.bankerprofile.save()

class FundPool(models.Model):
    pool_id = models.AutoField(primary_key=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    available_amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"Fund Pool {self.pool_id}"

    def add_contribution(self, amount):
        self.total_amount += amount
        self.available_amount += amount
        self.save()

class LoanFundApplication(models.Model):
    application_id = models.AutoField(primary_key=True)
    provider = models.ForeignKey(LoanProvider, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    duration_months = models.IntegerField(help_text="Duration in months",default=3)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    application_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    fund_pool = models.ForeignKey(FundPool, on_delete=models.CASCADE)

    def __str__(self):
        return f"Application {self.application_id} by {self.provider.name}"

    def calculate_payout_amount(self):
        return self.amount * (1 + (self.interest_rate / 100) * (self.duration_months / 12))


    def calculate_payout_date(self):
        # Calculate the payout date based on the duration
        return self.application_date + timedelta(days=self.duration_months * 30)

    def approve(self):
        payout_amount = self.calculate_payout_amount()
        payout_date = self.calculate_payout_date()

        # Calculate the future available amount in the fund pool
        future_available_amount = self.fund_pool.available_amount

        # Here you can implement more sophisticated logic to predict the available amount at the payout date
        # For simplicity, we'll assume no loans will be disbursed in the meantime

        if payout_amount <= future_available_amount:
            self.status = 'Approved'
            self.fund_pool.add_contribution(self.amount_requested)
            self.save()
        else:
            raise ValidationError(f"Insufficient funds: {payout_amount} requested, but only {future_available_amount} will be available at payout.")

class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in months")
    max_amount = models.DecimalField(max_digits=20, decimal_places=2)
    min_amount = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')])
    start_date = models.DateField()
    end_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')  
    personnel = models.ForeignKey(BankPersonnel, on_delete=models.CASCADE, related_name='managed_loans',blank=True, null=True)  
    fund_pool = models.ForeignKey(FundPool, on_delete=models.CASCADE,default=1)

    def clean(self):
        # Check if the loan amount exceeds the available amount in the fund pool
        if self.amount > self.fund_pool.available_amount:
            raise ValidationError(f"Loan amount {self.amount} exceeds the available fund pool amount {self.fund_pool.available_amount}.")

    def save(self, *args, **kwargs):
        # Run the clean method to enforce validation
        self.clean()

        # Reduce the available amount in the fund pool when a loan is approved
        if self.status == 'Approved':
            self.fund_pool.available_amount -= self.amount
            self.fund_pool.save()

        super(Loan, self).save(*args, **kwargs)

    def __str__(self):
        return f"Loan {self.loan_id} - {self.status}"

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    transaction_type = models.CharField(max_length=50, choices=[('Payment', 'Payment'), ('Disbursement', 'Disbursement')])
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Adjust the available amount in the fund pool based on the transaction type
        if self.transaction_type == 'Payment':
            self.loan.fund_pool.available_amount += self.amount
        elif self.transaction_type == 'Disbursement':
            self.loan.fund_pool.available_amount -= self.amount

        self.loan.fund_pool.save()
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.transaction_type}"
