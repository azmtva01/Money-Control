from django.db import models
from django.conf import settings


class Person(models.Model):
    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
        ordering = ['-id']

    som = "KGS"
    rub = "RUB"
    usd = "USD"
    CURRENCY_CHOICES = (
        (som, "KGS"),
        (rub, "RUB"),
        (usd, "USD")
    )
    name = models.CharField('Full name', max_length=128, blank=True, null=True)
    age = models.PositiveIntegerField('Age', blank=True, null=True)
    image = models.ImageField('Image', upload_to='image/', blank=True, null=True)
    user_profile = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='User Profile',
                                        on_delete=models.CASCADE, blank=True, null=True)
    total_account = models.IntegerField('Total account', default=0)
    auth_code = models.CharField('Code for sign in', max_length=4, blank=True, null=True)
    currency = models.CharField('Choice currency', max_length=3, choices=CURRENCY_CHOICES,
                                default='som', blank=True)


class Category(models.Model):

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['-id']

    income = "income"
    expense = "expense"

    Budget_choices = (
        (income, "income"),
        (expense, "expense"),
    )

    title = models.CharField('Title', max_length=128, blank=True, null=True)
    budget_choice = models.CharField('Budget Choice', max_length=7, choices=Budget_choices, default='expense', blank=True)
    person = models.ForeignKey(Person, verbose_name='User', on_delete=models.CASCADE,
                               blank=True, null=True)

    def __str__(self):
        return self.title


class Budget(models.Model):
    person = models.ForeignKey(Person, verbose_name='User', on_delete=models.CASCADE,
                               blank=True, null=True)
    income_value = models.PositiveIntegerField('Income value', default=0)
    expense_value = models.PositiveIntegerField('Expense value', default=0)
    category = models.ForeignKey(Category, verbose_name='category', on_delete=models.CASCADE,
                                 blank=True, null=True)
    added_date = models.DateTimeField('Added date', auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'
        ordering = ['-id']
