from django.db import models

import uuid


# Create your models here.
class BankAccount(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.CharField(unique=True, max_length=50)
    account_type = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=100)

    # @property
    # def full_number(self):
    #     return "-".join(self.bank_id, self.account_id, self.branch_id, )

    class Meta:
        verbose_name = "BankAccount"
        verbose_name_plural = "BankAccounts"

    def __str__(self):
        return "Account({})".format(self.account_id)
