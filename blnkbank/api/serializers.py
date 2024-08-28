from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import  User,BankPersonnel,LoanProvider,Customer,BankerProfile,LoanProviderProfile,CustomerProfile, FundPool, Loan, LoanFundApplication,Transaction


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'role',
            'date_of_birth',
            'address',
            'phone_number',
            'password',
        ]
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class BankerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankerProfile
        fields = ['banker_id']  

class LoanProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProviderProfile
        fields = ['LoanProvider_id']  

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['customer_id','credit_score']  
        
        
class BankPersonnelSerializer(UserSerializer):
    profile = BankerProfileSerializer(source='bankerprofile', read_only=True)

    class Meta(UserSerializer.Meta):
        model = BankPersonnel
        fields = UserSerializer.Meta.fields + ['profile']

class LoanProviderSerializer(UserSerializer):
    profile = LoanProviderProfileSerializer(source='loanproviderprofile', read_only=True)

    class Meta(UserSerializer.Meta):
        model = LoanProvider
        fields = UserSerializer.Meta.fields + ['profile']

class CustomerSerializer(UserSerializer):
    profile = CustomerProfileSerializer(source='customerprofile', read_only=True)
    credit_score = serializers.IntegerField()

    class Meta(UserSerializer.Meta):
        model = Customer
        fields = UserSerializer.Meta.fields + ['credit_score', 'profile']

        
class FundPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundPool
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class LoanFundApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanFundApplication
        fields = ('amount', 'interest_rate', 'duration_months','provider','status','fund_pool','application_id','application_date')
        
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        