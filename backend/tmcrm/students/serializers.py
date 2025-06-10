from rest_framework import serializers
from mainapp.serializers import BaseSerializerExcludeFields
from .models import *


class StudentGroupSerializer(BaseSerializerExcludeFields):

    class Meta:
        model = StudentGroup
        exclude = ['org', 'id']