from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework.reverse import reverse  

class CustomApiRoot(APIView):  
    def get(self, request):  
        return Response({  
            "students": reverse('students-list', request=request),  
            "schedule": reverse('schedule-list', request=request),  
            "financial_reporting": reverse('financial_reporting-list', request=request)
 
        })  