from rest_framework.permissions import BasePermission
from .models import Person


class IsPersonOwnerOrGet(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET' or request.method == 'POST' or request.method == 'OPTIONS':
            return True
        else:
            person = Person.objects.get(id=view.kwargs['pk'])
            return request.user == person.user_profile
