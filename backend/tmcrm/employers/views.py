from rest_framework.exceptions import ValidationError
from django.http import FileResponse
from rest_framework.permissions import BasePermission, IsAuthenticated
from .serializers.read import EmployerReadSerializer, TeacherReadSerializer, DepartmentReadSerializer, LeaveReadSerializer, TeacherNoteReadSerializer
from .serializers.write import EmployerWriteSerializer, TeacherWriteSerializer, DepartmentWriteSerializer, LeaveWriteSerializer, TeacherNoteWriteSerializer
from .serializers.other import DocumentsSerializer
from mainapp.views import BaseViewSetWithOrdByOrg, SelectRelatedViewSet
from .models import Teacher, Employer, Documents, Department, Leave, TeacherNote
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsTeacherProfile


class TeacherViewset(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    select_related_fields = []
    queryset = Teacher.objects.all()
    read_serializer_class = TeacherReadSerializer
    write_serializer_class = TeacherWriteSerializer


class EmployerViewSet(BaseViewSetWithOrdByOrg):
    queryset = Employer.objects.all()
    read_serializer_class = EmployerReadSerializer
    write_serializer_class = EmployerWriteSerializer


class DepartmentViewSet(BaseViewSetWithOrdByOrg):
    queryset = Department.objects.all()
    read_serializer_class = DepartmentReadSerializer
    write_serializer_class = DepartmentWriteSerializer


class DownloadDocumentViewset(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer

    @action(detail=False, methods=['get'])
    def response_documents(self, request):
        doc_id = request.query_params.get('id')
        if not doc_id:
            return Response({'detail': 'id required'}, status=400)

        try:
            doc = Documents.objects.get(id=doc_id)
        except Documents.DoesNotExist:
            return Response({'detail': 'Document not found'}, status=404)

        return FileResponse(doc.file_path.open(), filename=doc.file_path.name)


class LeaveViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Leave.objects.all()
    read_serializer_class = LeaveReadSerializer
    write_serializer_class = LeaveWriteSerializer


class TeacherNoteViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    select_related_fields = ["teacher_profile", ]
    queryset = TeacherNote.objects.all()
    read_serializer_class = TeacherNoteReadSerializer
    write_serializer_class = TeacherNoteWriteSerializer

    def get_permissions(self) -> list[BasePermission]:
        return [IsAuthenticated(), IsTeacherProfile()]

    def perform_create(self, serializer):
        teacher_profile = self.request.user.get_teacher_profile()
        super().perform_create(serializer, teacher_profile=teacher_profile)
