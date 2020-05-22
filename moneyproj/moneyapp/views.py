from datetime import datetime
from collections import OrderedDict
from django.contrib.auth.models import User
from rest_framework import filters, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
import django_filters.rest_framework
from .models import Person, Budget, Category
from .permissions import IsPersonOwnerOrGet
from .serializers import PersonSerializer, BudgetSerializer, CategorySerializer, ExpenseSerializer, IncomeSerializer
from .utils import generete_code


class RegisterView(APIView):

    @staticmethod
    def post(request):
        phone_number = request.data.get('phone_number')
        if phone_number:
            user = User.objects.create(username=phone_number)
            Token.objects.create(user=user)
            code = generete_code()
            profile = Person.objects.create(user_profile=user, auth_code=code)
            """ToDo SMS"""
            return Response('REGISTERED', status=status.HTTP_201_CREATED)
        return Response('ERROR', status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    @staticmethod
    def post(request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        if phone_number and code:
            user = User.objects.get(username=phone_number)
            profile = Person.objects.get(user_profile=user)
            if code == profile.auth_code:
                new_code = generete_code()
                profile.auth_code = new_code
                profile.save()
                token = Token.objects.get(user=user)
                return Response(f'{token.key}', status=status.HTTP_200_OK)
            return Response('WRONG CODE', status=status.HTTP_400_BAD_REQUEST)
        return Response('NEED FULL DATA', status=status.HTTP_400_BAD_REQUEST)


class CheckPhoneView(APIView):

    @staticmethod
    def post(request):
        phone_number = request.data.get('phone_number')
        if phone_number:
            if User.objects.filter(username=phone_number):
                user = User.objects.get(username=phone_number)
                profile = Person.objects.get(user_profile=user)
                code = profile.auth_code
                """ToDo SMS"""
                return Response('WE HAVE THIS NUMBER IN DB', status=status.HTTP_200_OK)
            return Response('WE DO NOT HAVE THIS NUMBER IN DB', status=status.HTTP_400_BAD_REQUEST)
        return Response('YOUR PHONE PLEASE', status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    @staticmethod
    def post(request):
        phone_number = request.data.get('phone_number')
        if phone_number:
            user = User.objects.get(username=phone_number)
            token = Token.objects.get(user=user)
            token.delete()
            user.delete()
        return Response('YOU ARE LOGGED OUT', status=status.HTTP_200_OK)


class PersonView(ModelViewSet):
    filter_backends = ([django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter])
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsPersonOwnerOrGet]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    lookup_field = 'pk'
    filter_fields = ('name',)
    search_fields = ('name',)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request_user'] = self.request.user
        return context


class BudgetListView(ModelViewSet):
    filter_backends = ([django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter])
    authentication_classes = [TokenAuthentication]
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()
    lookup_field = 'pk'
    filter_fields = ('person', 'category')
    search_fields = ('person',)


class MyBudgetView(ModelViewSet):
    filter_backends = ([django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter])
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()
    lookup_field = 'pk'
    filter_fields = ('income_value', 'category', 'expense_value',)
    search_fields = ('person', 'category',)

    def get_queryset(self, *args, **kwargs):
        queryset = Budget.objects.filter(person=self.request.user.person)
        order_field = self.request.GET.get('order')
        filter_fields = {}

        if order_field:
            queryset = queryset.order_by(order_field)
            return queryset

        if filter_fields:
            queryset = queryset.filter(**filter_fields)
            return queryset

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('start_date')
        category = self.request.GET.get('category')

        if category:
            queryset = queryset.filter(category=category)

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%d.%m.%Y').date()
            end_date = datetime.strptime(end_date, '%d.%m.%Y').date()
            queryset = queryset.filter(added_date__date__gte=start_date, added_date__date__lte=end_date)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        person = Person.objects.get(user_profile=request.user)
        serializer.save()
        if int(request.data['income_value']) > 0 and int(request.data['expense_value']) > 0:
            print(request.data['income_value'])
            person.total_account += int(request.data['income_value'])
            person.total_account -= int(request.data['expense_value'])
            person.save()
            print(request.data['expense_value'])
        elif int(request.data['income_value']) == 0:
            person.total_account -= int(request.data['expense_value'])
            person.save()
        elif int(request.data['expense_value']) == 0:
            person.total_account += int(request.data['income_value'])
            person.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        person = Person.objects.get(user_profile=request.user)
        budget = self.get_object()
        serializer = self.get_serializer(instance=budget, data=request.data)
        serializer.is_valid(raise_exception=True)
        if int(request.data['income_value']) > 0 and int(request.data['expense_value']) > 0:
            person.total_account -= int(budget.income_value)
            person.total_account += int(budget.expense_value)
            person.total_account += int(request.data['income_value'])
            person.total_account -= int(request.data['expense_value'])
            person.save()
        elif request.data['income_value'] == 0:
            person.total_account += int(budget.expense_value)
            person.total_account -= int(request.data['expense_value'])
            person.save()
        elif request.data['expense_value'] == 0:
            person.total_account -= int(budget.income_value)
            person.total_account += int(request.data['income_value'])
            person.save()
        elif request.data['expense_value'] == 0 and request.data['income_value'] == 0:
            person.total_account -= int(budget.income_value)
            person.total_account += int(budget.expense_value)
            person.total_account += int(request.data['income_value'])
            person.total_account -= int(request.data['expense_value'])
            person.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        person = instance.person
        if instance.income_value > 0 and instance.expense_value > 0:
            person.total_account -= int(instance.income_value)
            person.total_account += int(instance.expense_value)
            person.save()
        elif instance.income_value == 0:
            person.total_account += int(instance.expense_value)
            person.save()
        elif instance.expense_value == 0:
            person.total_account -= int(instance.income_value)
            person.save()
        instance.delete()


class CategoryView(ModelViewSet):
    filter_backends = ([django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter])
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'pk'
    filter_fields = ('title',)
    search_fields = ('title',)

    def get_queryset(self,  *args, **kwargs):
        queryset = Category.objects.filter(person=self.request.user.person)
        order_field = self.request.GET.get('order')
        filter_fields = {}

        if order_field:
            queryset = queryset.order_by(order_field)
            return queryset

        if filter_fields:
            queryset = queryset.filter(**filter_fields)
            return queryset

        budget_choice = self.request.GET.get('budget_choice')

        if budget_choice:
            queryset = queryset.filter(budget_choice=budget_choice)

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('start_date')

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%d.%m.%Y').date()
            end_date = datetime.strptime(end_date, '%d.%m.%Y').date()
            queryset = queryset.filter(added_date__date__gte=start_date, added_date__date__lte=end_date)
        return queryset

    def my_categories(self, request):
        queryset = Category.objects.filter(person=request.user.person)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class IncomeView(ModelViewSet):
    filter_backends = ([django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter])
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IncomeSerializer
    queryset = Budget.objects.all()
    lookup_field = 'pk'
    filter_fields = ('category', 'income_value',)
    search_fields = ('person', 'category',)

    def get_queryset(self, *args, **kwargs):
        queryset = Budget.objects.filter(person=self.request.user.person)
        order_field = self.request.GET.get('order')
        filter_fields = {}

        if order_field:
            queryset = queryset.order_by(order_field)
            return queryset

        if filter_fields:
            queryset = queryset.filter(**filter_fields)
            return queryset

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('start_date')
        category = self.request.GET.get('category')

        if category:
            queryset = queryset.filter(category=category)

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%d.%m.%Y').date()
            end_date = datetime.strptime(end_date, '%d.%m.%Y').date()
            queryset = queryset.filter(added_date__date__gte=start_date, added_date__date__lte=end_date)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        person = Person.objects.get(user_profile=request.user)
        serializer.save()
        if int(request.data['income_value']):
            person.total_account += int(request.data['income_value'])
            person.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        person = Person.objects.get(user_profile=request.user)
        budget = self.get_object()
        serializer = self.get_serializer(instance=budget, data=request.data)
        serializer.is_valid(raise_exception=True)
        if int(request.data['income_value']):
            person.total_account -= int(budget.income_value)
            person.total_account += int(request.data['income_value'])
            person.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        person = instance.person
        if instance.income_value:
            person.total_account -= int(instance.income_value)
            person.save()
        instance.delete()


class ExpenseView(ModelViewSet):
    filter_backends = ([django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter])
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    serializer_class = ExpenseSerializer
    queryset = Budget.objects.all()
    lookup_field = 'pk'
    filter_fields = ('category', 'expense_value',)
    search_fields = ('person', 'category',)

    def get_queryset(self, *args, **kwargs):
        queryset = Budget.objects.filter(person=self.request.user.person)
        order_field = self.request.GET.get('order')
        filter_fields = {}

        if order_field:
            queryset = queryset.order_by(order_field)
            return queryset

        if filter_fields:
            queryset = queryset.filter(**filter_fields)
            return queryset

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('start_date')
        category = self.request.GET.get('category')

        if category:
            queryset = queryset.filter(category=category)

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%d.%m.%Y').date()
            end_date = datetime.strptime(end_date, '%d.%m.%Y').date()
            queryset = queryset.filter(added_date__date__gte=start_date, added_date__date__lte=end_date)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        person = Person.objects.get(user_profile=request.user)
        serializer.save()
        if int(request.data['expense_value']):
            person.total_account -= int(request.data['expense_value'])
            person.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        person = Person.objects.get(user_profile=request.user)
        budget = self.get_object()
        serializer = self.get_serializer(instance=budget, data=request.data)
        serializer.is_valid(raise_exception=True)
        if int(request.data['expense_value']):
            person.total_account += int(budget.expense_value)
            person.total_account -= int(request.data['expense_value'])
            person.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        person = instance.person
        if instance.expense_value:
            person.total_account += int(instance.expense_value)
            person.save()
        instance.delete()


class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 200

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_count', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
