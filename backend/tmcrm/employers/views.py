from django.http import Http404
from django.shortcuts import render
from employers.serializers import TeacherSerializer, EmployerSerializer, DocumentsSerializer
from mainapp.views import BaseViewSetWithOrdByOrg, SelectRelatedViewSet
from .models import Teacher, Employer, Documents
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from django.http import FileResponse, Http404, HttpResponse
from rest_framework.response import Response
import zipfile
import io
import os



class TeacherViewset(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    select_related_fields = []

    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class EmployerViewSet(BaseViewSetWithOrdByOrg):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer


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
