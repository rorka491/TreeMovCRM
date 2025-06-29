from rest_framework import serializers
from .models import SubjectColor


class BaseSerializerExcludeFields(serializers.ModelSerializer):
    """
    Класс при наследовании дает возможность указать какмие поля можно исключить 
    передав аргумент exclude_fields
    Например:

    class GroupScheduleSerializer(ScheduleStudentGroupSerializer):
        group = StudentGroupSerializer(exclude_fields=['students'])
        exclude_fields = ['group']

        class Meta: 
            fields = ['group', 'schedules']

    таким образом группа будет сереализоована без студентов
    """
    class Meta:
        model = None
        exclude = ['org', 'created_by']

    def __init__(self, instance=None, *args, **kwargs):
        

        #передан instance чтобы сохранить совместимостсь с DRF
        meta_excludes = getattr(self.Meta, 'exclude_fields', [])

        un_exclude_fields = kwargs.pop('un_exclude_fields', [])
        exclude_fields = kwargs.pop('exclude_fields', []) + meta_excludes

        super().__init__(instance, *args, **kwargs)

        if not un_exclude_fields:

            #Нужно чтобы исключить те поля которые есть в списке
            for field in exclude_fields:
                self.fields.pop(field, None)
        
        else:
            for field in list(self.fields):
                if field not in un_exclude_fields:
                    self.fields.pop(field)


class ColorSerializer(BaseSerializerExcludeFields):

    class Meta(BaseSerializerExcludeFields.Meta):
        model = SubjectColor


