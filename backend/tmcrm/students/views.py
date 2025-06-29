from django.shortcuts import render
from mainapp.views import BaseViewSetWithOrdByOrg, SelectRelatedViewSet, base_search
from .models import *
from .serializers import *
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response
import django_filters
from lesson_schedule.serializers import GradeSerializer
from lesson_schedule.models import Grade



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
        return q
    
class StudentGradeViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.kwargs.get('student_pk')

        if student_id:
            queryset = queryset.filter(student_id=student_id).order_by('-created_at')
        else:
            queryset = queryset.all().order_by('-created_at')

        last = self.request.query_params.get('last')
        if last:
            try:
                last = int(last)
                queryset = queryset[:last]  # обязательно присваиваем
            except ValueError:
                pass  # если не число — игнорируем

        return queryset







class ParentViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Parent.objects.all()
    prefetch_related_fields = ['child']
    serializer_class = ParentSerializer 
    