from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from mainapp.views import BaseViewSetWithOrdByOrg, SelectRelatedViewSet, base_search
from lesson_schedule.models import Grade
from lesson_schedule.serializers.read import GradeReadSerializer
from .models import StudentGroup, Student
from students.models import Parent
from .serializers.read import StudentGroupReadSerializer, StudentReadSerializer, ParentReadSerializer
from .serializers.write import StudentGroupWriteSerializer, StudentWriteSerializer, ParentWriteSerializer



class StudentGroupViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = StudentGroup.objects.all()
    read_serializer_class = StudentGroupReadSerializer
    write_serializer_class = StudentGroupReadSerializer
    prefetch_related_fields = ['students']


    @action(detail=False, methods=['post'], url_path='search')
    @base_search
    def search(self, request, words: list[str]) -> Q:
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
    read_serializer_class = StudentReadSerializer
    write_serializer_class = StudentWriteSerializer

    @action(detail=False, methods=["get"], url_path="get_count_students")
    def get_count_students(self, request):
        count_students = super().get_queryset().count()
        return Response({"count": count_students})

    @action(detail=False, methods=["post"], url_path="search")
    @base_search
    def search(self, request, words: list[str]) -> Q:
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
    read_serializer_class = GradeReadSerializer
    write_serializer_class = GradeReadSerializer



class ParentViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Parent.objects.all()
    prefetch_related_fields = ['child']
    read_serializer_class = ParentReadSerializer
    write_serializer_class = ParentWriteSerializer
