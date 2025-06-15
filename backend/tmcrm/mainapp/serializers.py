from rest_framework import serializers


class BaseSerializerWithoutOrg(serializers.ModelSerializer):
    """
    Пока этот класс бесполезен
    """
    class Meta:
        exclude = ['id', 'org']

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
        fields = '__all__'

    def __init__(self, instance=None, *args, **kwargs):
        

        #передан instance чтобы сохранить совместимостсь с DRF
        meta_excludes = getattr(self.Meta, 'exclude_fields', [])
        exclude_fields = kwargs.pop('exclude_fields', []) + meta_excludes
        
        super().__init__(instance, *args, **kwargs)

        #Нужно чтобы исключить те поля которые есть в списке
        for field in exclude_fields:
            self.fields.pop(field, None)


