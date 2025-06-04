from rest_framework import serializers


class BaseSerilizeWithOutOrg(serializers.ModelSerializer):
    class Meta:
        exclude = ['id', 'org']

class BaseSerializerExcludeFields(serializers.ModelSerializer):

    def __init__(self, instance=None, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude_fields', [])
        
        super().__init__(instance, *args, **kwargs)

        for field in exclude_fields:
            self.fields.pop(field, None)


