from mainapp.serializers import BaseSerializerExcludeFields
from .read import EmployerReadSerializer
from employers.models import Documents, DocumentsTypes

class DocumentsTypesSerializer(BaseSerializerExcludeFields):

    class Meta(BaseSerializerExcludeFields.Meta):
        model = DocumentsTypes


class DocumentsSerializer(BaseSerializerExcludeFields):
    employer = EmployerReadSerializer(read_only=True)
    doc_type = DocumentsTypesSerializer(read_only=True)

    class Meta(BaseSerializerExcludeFields.Meta):
        model = Documents

