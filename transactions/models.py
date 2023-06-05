import datetime
from decimal import Decimal
from django.db import models
from django.utils import timezone

import uuid


# 11.4.4.1 <STMTTRN>
# https://financialdataexchange.org/common/Uploaded%20files/OFX%20files/OFX%20Banking%20Specification%20v2.3.pdf

# class BankAccount(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     account_id = models.CharField(unique=True, max_length=50)
#     account_type = models.CharField(max_length=50, null=True)
#     # institution = models.CharField(max_length=50, null=True)
#     # balance = models.DecimalField(max_digits=10, decimal_places=2)
#     # balance_date = models.DateTimeField()
#     # balance_user_date = models.DateTimeField()
#     currency = models.CharField(max_length=50)
#     institution = models.CharField(max_length=50)
#     description = models.CharField(max_length=50)
#     # user_id = models.CharField(max_length=50)

#     class Meta:
#         verbose_name = "Account"
#         verbose_name_plural = "Accounts"

#     def __str__(self):
#         return "Account({})".format(self.id)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_id = models.CharField(unique=True, max_length=50)
    transaction_type = models.CharField(max_length=50)
    payee = models.CharField(max_length=100)
    date = models.DateTimeField()
    user_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    memo = models.CharField(max_length=50, blank=True, null=True)
    sic = models.CharField(max_length=50, blank=True, null=True)
    mcc = models.CharField(max_length=50, blank=True, null=True)
    checknum = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        # unique_together = ("transaction_id", )

    def __str__(self):
        return "Transaction({})".format(self.id)
