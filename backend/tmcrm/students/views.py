from django.shortcuts import render
from mainapp.views import BaseViewSetWithOrdByOrg, SelectRelatedViewSet, base_search
from .models import *
from .serializers import *
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response



class StudentGroupViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer

    prefetch_related_fields = ['students']

    @action(detail=False, methods=['post'], url_path='search')
    @base_search
    def search(self, request, words: list[str]):
        q = Q()
        for word in words:
            q |= (
            Q(students__name__icontains=word) |
            Q(students__surname__icontains=word) |
            Q(name__icontains=word)
            )  
        return q


class StudentViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    @action(detail=False, methods=['post'], url_path='search')
    @base_search
    def search(self, request, words: list[str]):
        q = Q()
        for word in words:
            q |= (
                Q(name__icontains=word) |
                Q(surname__icontains=word) |
                Q(phone_number__icontains=word) |
                Q(birthday__icontains=word) |
                Q(email__icontains=word)
            )
        return 
