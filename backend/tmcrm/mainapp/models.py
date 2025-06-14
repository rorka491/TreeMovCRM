from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator



phone_number_regex = RegexValidator(
    regex=r'^8\d{10}$',
    message='Телефон должен быть в формате 8 XXX XXX XX XX '
)

color_regex = RegexValidator(
    regex=r'^#[0-9A-Fa-f]{6}$',
    message='Неверный формат цвета'
)



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
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    

class BaseModelOrg(models.Model): 
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        abstract = True


    def clean(self):
        errors = {}

        for field in self._meta.get_fields():

            if isinstance(field, (models.ForeignKey, models.OneToOneField)):
                related_obj = getattr(self, field.name, None)
                
                if related_obj and hasattr(related_obj, 'org'):
                    
                    related_org = getattr(related_obj, 'org', None)
                    if related_org != self.org:
                        errors[field.name] = (
                            f"Поле '{field.name}' ссылается на объект с другой организации: "
                            f" (ожидалось: {related_org})"
                        )
        if errors:
            raise ValidationError(errors)
        
    def save(self, *args, **kwargs):
        org = kwargs.get('org', None)
        if org:
            self.org = org

        super().save(*args, **kwargs)

    @classmethod
    def create_with_user_org(cls, user, **kwargs):
        obj = cls(**kwargs)
        obj.save(org=user.org)
        return obj



class SubjectColor(BaseModelOrg):
    title = models.CharField(max_length=30, null=True)
    color_hex = models.CharField(max_length=7, validators=[color_regex])
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Цвет предмета'
        verbose_name_plural = 'Цвета предметов'

    def __str__(self):
        return f'{self.title}'



