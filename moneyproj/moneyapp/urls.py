from django.urls import path
from moneyapp.views import PersonView, MyBudgetView, CategoryView, \
    BudgetListView, RegisterView, LoginView, CheckPhoneView, LogoutView, \
    ExpenseView, IncomeView

urlpatterns = [
    path('category/', CategoryView.as_view({'get': 'list', 'post': 'create'})),
    path('category/<int:pk>/', CategoryView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('person/', PersonView.as_view({'get': 'list', 'post': 'create'})),
    path('person/<int:pk>/', PersonView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('budget/list/', BudgetListView.as_view({'get': 'list', 'post': 'create'})),
    path('budget/list/<int:pk>/', BudgetListView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('my_budget/', MyBudgetView.as_view({'get': 'list', 'post': 'create'})),
    path('my_budget/<int:pk>/', MyBudgetView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('income/', IncomeView.as_view({'get': 'list', 'post': 'create'})),
    path('income/<int:pk>/', IncomeView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('expense/', ExpenseView.as_view({'get': 'list', 'post': 'create'})),
    path('expense/<int:pk>/', ExpenseView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('my_categories/', CategoryView.as_view({'get': 'list', 'post': 'create'})),

    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('check_phone/', CheckPhoneView.as_view()),
    path('logout/', LogoutView.as_view()),
]