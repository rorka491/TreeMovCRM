from django.core.validators import RegexValidator



phone_number_regex = RegexValidator(
    regex=r'^8\d{10}$',
    message='Телефон должен быть в формате 8 XXX XXX XX XX '
)

color_regex = RegexValidator(
    regex=r'^#[0-9A-Fa-f]{6}$',
    message='Неверный формат цвета'
)
