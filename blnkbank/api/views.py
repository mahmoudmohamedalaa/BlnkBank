from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from .models import Loan, Transaction, FundPool, LoanProvider, LoanFundApplication
from .serializers import LoanSerializer, TransactionSerializer, FundPoolSerializer, LoanProviderSerializer, LoanFundApplicationSerializer,UserSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


User = get_user_model()

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = response.data
        user_instance = User.objects.get(username=user['username'])
        token, created = Token.objects.get_or_create(user=user_instance)
        
        print(f"User role: {user_instance.role}")

        return Response({
            'token': token.key,
            'user': user,
        }, status=status.HTTP_201_CREATED)

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        user = authenticate(username=serializer.validated_data['username'],
                    password=serializer.validated_data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            if user.role == 'CUSTOMER':
                redirect_url = reverse('customer_dashboard')
            elif user.role == 'LOANPROVIDER':
                redirect_url = reverse('loan_provider_dashboard')
            elif user.role == 'BANKPERSONNEL':
                redirect_url = reverse('bank_personnel_dashboard')
        
            return Response({
                
                'token': token.key,
                'user_type': user.role,
                'redirect_url': redirect_url
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)




class CustomerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'CUSTOMER':
            return Response({'detail': 'You do not have permission to access this.'}, status=403)
        loans = Loan.objects.filter(customer=request.user)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        loan_id = request.data.get('loan_id')
        amount = request.data.get('amount')

        loan = get_object_or_404(Loan, loan_id=loan_id, customer=request.user)

        transaction = Transaction.objects.create(
            transaction_date=request.data.get('transaction_date'),
            amount=amount,
            transaction_type='Payment',
            loan=loan,
            customer=request.user
        )

        transaction_serializer = TransactionSerializer(transaction)
        return Response(transaction_serializer.data, status=201)

class LoanProviderDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'LOANPROVIDER':
            return Response({'detail': 'You do not have permission to access this.'}, status=403)
        applications = LoanFundApplication.objects.filter(provider=request.user)
        serializer = LoanFundApplicationSerializer(applications, many=True)
        return Response(serializer.data)

class BankPersonnelDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'BANKPERSONNEL':
            return Response({'detail': 'You do not have permission to access this.'}, status=403)
        loan_fund_applications = LoanFundApplication.objects.all()
        loans = Loan.objects.all()

        loan_fund_serializer = LoanFundApplicationSerializer(loan_fund_applications, many=True)
        loan_serializer = LoanSerializer(loans, many=True)

        return Response({
            "loan_fund_applications": loan_fund_serializer.data,
            "loans": loan_serializer.data
        })

    def post(self, request):
        # implement logic to approve or reject loan applications
        pass




