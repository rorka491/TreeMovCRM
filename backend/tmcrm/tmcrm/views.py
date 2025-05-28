from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework.reverse import reverse  

class CustomApiRoot(APIView):  
    def get(self, request):  
        return Response({  
            "students": reverse('students-list', request=request),  
            "schedules": reverse('schedules-list', request=request),  
            "subjects": reverse('subjects-list', request=request),  
            "attendances": reverse('attendances-list', request=request),  
            "grades": reverse('grades-list', request=request),              
            "financial_reporting": reverse('financial_reporting-list', request=request),
            "employers": reverse('employer-list', request=request),  


        })  
