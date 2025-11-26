from typing import Type
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Organization, SubjectColor
from .constants import HttpMethodLiteral


class BaseSerializerExcludeFields(serializers.ModelSerializer):
    """
    Класс при наследовании дает возможность указать какмие поля можно исключить 
    передав аргумент exclude_fields
    Например:

    class GroupScheduleSerializer(ScheduleStudentGroupSerializer):
        group = StudentGroupSerializer(exclude_fields=['students'])
 
        class Meta: 
            fields = ['group', 'schedules']

    таким образом группа будет сереализована без студентов
    """

    def __init__(self, instance=None, *args, **kwargs):
        # передан instance чтобы сохранить совместимостсь с DRF
        meta_excludes = getattr(self.Meta, 'exclude_fields', [])

        un_exclude_fields = kwargs.pop('un_exclude_fields', [])
        exclude_fields = kwargs.pop('exclude_fields', []) + meta_excludes

        super().__init__(instance, *args, **kwargs)

        if not un_exclude_fields:

            # Нужно чтобы исключить те поля которые есть в списке
            for field in exclude_fields:
                self.fields.pop(field, None)

        else:
            for field in list(self.fields):
                if field not in un_exclude_fields:
                    self.fields.pop(field)

    class Meta:
        model = None
        fields = '__all__'

class BaseReadSerializer(BaseSerializerExcludeFields):
    def __init__(self, *args, **kwargs): # Все поля по умолчанию read_only
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.read_only = True

    class Meta(BaseSerializerExcludeFields.Meta):
        ...

class BaseWriteSerializer(BaseSerializerExcludeFields):

    class Meta(BaseSerializerExcludeFields.Meta):
        exclude = ['org', 'created_by', 'created_at']
        fields = None



class ColorSerializer(BaseSerializerExcludeFields):

    class Meta(BaseSerializerExcludeFields.Meta):
        model = SubjectColor


class OrganizationReadSerializer(BaseReadSerializer):
    
    class Meta(BaseReadSerializer.Meta):
        model = Organization


class OrganizationWriteSerializer(BaseWriteSerializer):

    class Meta(BaseWriteSerializer.Meta):
        model = Organization
        exclude = ["created_by"]


class RegisterStartSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(min_length=5, max_length=60, required=True)
    password = serializers.CharField(min_length=10, required=True)

    def validate_username(self, username):
        username = username.strip()
        User = get_user_model()

        if " " in username:
            raise serializers.ValidationError("Username must not contain spaces")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(f'Username: "{username}" is taken')
        return username

    def validate_email(self, email):
        email = email.strip()
        User = get_user_model()

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(f'Email: "{email}" is taken')
        return email


class RegeisterConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True, max_length=6, min_length=6)


