from django.shortcuts import render
from rest_framework import viewsets  
from .models import *  
from .serializers import *


class StudentViewSet(viewsets.ModelViewSet):  
    queryset = Student.objects.all()  
    serializer_class = StudentSerializer  


class StudentGroupViewSet(viewsets.ModelViewSet):  
    queryset = StudentGroup.objects.all()  
    serializer_class = StudentGroupSerializer   


class ParentViewSet(viewsets.ModelViewSet):  
    queryset = Parent.objects.all()  
    serializer_class = ParentSerializer   