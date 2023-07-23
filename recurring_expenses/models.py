from django.db import models
from uuid import uuid4
from bank_accounts.models import BankAccount


class RecurringExpense(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    active = models.BooleanField(default=True)
    particulars = models.CharField(max_length=256)
    currency = models.CharField(max_length=3)
    period = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True, blank=True)
