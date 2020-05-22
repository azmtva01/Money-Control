from rest_framework import serializers
from .models import Person, Budget, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'budget_choice', 'id')

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        person = Person.objects.get(user_profile=self.context['request'].user)
        category.person = person
        category.save()
        return category


class PersonSerializer(serializers.ModelSerializer):
    user_profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Person
        fields = ('name', 'age', 'image', 'currency', 'user_profile', 'auth_code', 'total_account', 'id')

    def create(self, validated_data):
        person = Person.objects.create(**validated_data)
        person.user_profile = self.context['request_user']
        person.save()
        print(self.context['request_user'])
        return person


class BudgetSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(read_only=True)
    added_date = serializers.DateTimeField(read_only=True, format='%d.%m.%y %H:%M')
    # category = serializers.SlugRelatedField(slug_field="title", read_only=True)

    class Meta:
        model = Budget
        fields = ('person', 'income_value', 'expense_value', 'category', 'added_date', 'id')

    def create(self, validated_data):
        budget = Budget.objects.create(**validated_data)
        person = Person.objects.get(user_profile=self.context['request'].user)
        budget.person = person
        budget.save()
        return budget


class IncomeSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(read_only=True)
    added_date = serializers.DateTimeField(read_only=True, format='%d.%m.%y %H:%M')

    class Meta:
        model = Budget
        fields = ('person', 'income_value', 'category', 'added_date', 'id')

    def create(self, validated_data):
        budget = Budget.objects.create(**validated_data)
        person = Person.objects.get(user_profile=self.context['request'].user)
        budget.person = person
        budget.save()
        return budget


class ExpenseSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(read_only=True)
    added_date = serializers.DateTimeField(read_only=True, format='%d.%m.%y %H:%M')

    class Meta:
        model = Budget
        fields = ('person', 'expense_value', 'category', 'added_date', 'id')

    def create(self, validated_data):
        budget = Budget.objects.create(**validated_data)
        person = Person.objects.get(user_profile=self.context['request'].user)
        budget.person = person
        budget.save()
        return budget
