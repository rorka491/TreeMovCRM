from django.shortcuts import render
from mainapp.views import BaseViewSetWithOrdByOrg, SelectRelatedViewSet, base_search
from .models import StudentGroup
from .serializers import StudentGroupSerializer


class StudentGroupViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer






