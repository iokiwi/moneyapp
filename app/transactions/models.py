from django.db import models

import uuid

from bank_accounts.models import BankAccount

# 11.4.4.1 <STMTTRN>
# https://financialdataexchange.org/common/Uploaded%20files/OFX%20files/OFX%20Banking%20Specification%20v2.3.pdf


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_id = models.CharField(unique=True, max_length=50)
    transaction_type = models.CharField(max_length=50)
    payee = models.CharField(max_length=100)
    payee_slug = models.SlugField(max_length=100, blank=True, null=True)
    date = models.DateTimeField()
    user_date = models.DateTimeField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    memo = models.CharField(max_length=50, blank=True, null=True)
    sic = models.CharField(max_length=50, blank=True, null=True)
    mcc = models.CharField(max_length=50, blank=True, null=True)
    checknum = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        data = {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "transaction_type": self.transaction_type,
            "payee_slug": self.payee_slug,
            "payee": self.payee,
            "date": self.date,
            "user_date": self.user_date,
            "amount": self.amount,
            "memo": self.memo,
            "sic": self.sic,
            "mcc": self.mcc,
            "checknum": self.checknum,
        }
        return "Transaction({})".format(data)
