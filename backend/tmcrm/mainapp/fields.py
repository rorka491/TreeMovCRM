from django.db import models
from django.core.exceptions import ValidationError


class MonthDayField(models.Field):
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 5
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        # Храним как VARCHAR(5) (формат 'MM-DD')
        return 'char(5)'

    def to_python(self, value):
        """Метод который позволяет питону получить 
        запись из базы в нужном формате DateFieldExcludeYear"""
        from .utils import DateFieldExcludeYear
        if value is None:
            return None
        if isinstance(value, DateFieldExcludeYear):
            return value
        if isinstance(value, str):
            try:
                month, day = map(int, value.split('-'))
                return DateFieldExcludeYear(month, day)
            except Exception:
                raise ValidationError('Неверный формат даты ожидается MM-DD')
        
        raise ValidationError("Неверный тип данных для MonthDayField")
    
    def get_prep_value(self, value):
        """Нужна для сохранения в базу, переносит данные в формат строки"""
        from .utils import DateFieldExcludeYear
        if value is None:
            return None
        if isinstance(value, DateFieldExcludeYear):
            return value.__repr__()
        if isinstance(value, str):
            return value
        raise ValidationError('неверный тип данных для сохраниния')
    

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return self.to_python(value)
    



