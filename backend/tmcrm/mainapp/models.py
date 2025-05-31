from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = 'Организация' 
        verbose_name_plural = 'Организации' 

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLES = (
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('user', 'Пользователь'),
    )
    
    role = models.CharField(max_length=20, choices=ROLES, default='user')
    org = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='users'
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
    )
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    

class BaseModelOrg(models.Model): 
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        abstract = True
    
