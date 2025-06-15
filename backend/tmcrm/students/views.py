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

    # @action(detail=False, methods=['post'], url_path='search')
    # @base_search
    # def search(self, request, query=None):
    #     words = query.split()
    #     q = Q()

    #     for word in words:
    #         q &= (
    #         Q(student__name__icontains=word) |
    #         Q(student__surname__icontains=word) |
    #         Q(student__name__icontains=word) |
    #         Q()
    #         )



class StudentViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    @action(detail=False, methods=['post'], url_path='search')
    @base_search
    def search(self, request, query=None):
        q = Q()

        for word in query:
            q |= (
                Q(name__icontains=word) |
                Q(surname__icontains=word) |
                Q(phone_number__icontains=word) |
                Q(birthday__icontains=word) |
                Q(email__icontains=word)
            )

        results = self.get_queryset().filter(q)
        serializer = self.serializer_class(results, many=True)
        return Response(serializer.data)