from rest_framework import serializers
from .models import *


class EmployerSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Employer  
        fields = '__all__'




class TeacherSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Teacher  
        fields = ['employer']  

    def to_representation(self, instance):  
        return {  
            'id': instance.employer.id,  
            'name': instance.employer.name,  
            'surname': instance.employer.surname  
        }  

'''
class TeacherSerializer(serializers.ModelSerializer):  
    # Получаем данные из Employer через OneToOneField  
    employer = EmployerSerializer()  

    class Meta:  
        model = Teacher  
        fields = ['employer']  

    def to_representation(self, instance):  
        # Возвращаем данные из Employer, а не вложенную структуру  
        data = super().to_representation(instance)  
        return data['employer']  
'''

'''
class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'
    

class TeacherSerializer(serializers.ModelSerializer):  
    employer = EmployerSerializer()  # Получаем данные из Employer  

    class Meta:  
        model = Teacher  
        fields = '__all__'  #['employer'] 
        
'''