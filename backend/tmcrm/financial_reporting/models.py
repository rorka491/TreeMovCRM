from django.db import models
from students.models import * 


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    method = models.CharField(max_length=50)
    comment = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'Платёж {self.amount} от {self.student.name} ({self.date})'


class Expense(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=100)
    comment = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'

    def __str__(self):
        return f'{self.title} — {self.amount} ({self.date})'


class Account(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='account')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Пополнение'),
        ('expense', 'Списание'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(auto_now_add=True)