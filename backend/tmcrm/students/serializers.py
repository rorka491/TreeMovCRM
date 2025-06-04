from rest_framework import serializers
from mainapp.serializers import BaseSerializerExcludeFields
from .models import *


class GroupSerializer(BaseSerializerExcludeFields):

    class Meta:
        model = StudentGroup
        exclude = ['org', 'id']