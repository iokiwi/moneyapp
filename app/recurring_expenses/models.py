import requests

from django.db import models
from uuid import uuid4
from bank_accounts.models import BankAccount
from memoize import memoize


# TODO(caching exchange rates)
# from django.core.cache import cache
# https://docs.djangoproject.com/en/4.2/topics/cache/=


def invert_rates(rates):
    return {k: 1 / v for k, v in rates.items()}


@memoize(timeout=60 * 60)  # cache for 1 hour
def get_exchange_rates(target_currency="NZD"):
    # Note, the API gives us from NZD -> everything so
    # we invert it to get everything -> NZD
    url = f"https://api.exchangerate-api.com/v4/latest/{target_currency}"
    response = requests.get(url)
    return invert_rates(response.json()["rates"])


def get_exchange_rate(currency_from, currency_to="NZD"):
    # TODO: Caching
    # https://docs.djangoproject.com/en/4.2/topics/cache/

    # rate = cache.get(currency_from)
    # # Update cache if miss
    # if rate is None:
    #     print("cache miss")
    #     rates = get_exchange_rates()
    #     for k, v in rates.items():
    #         # Store the rate in cache for 12 hours
    #         key = f"{k}{currency_to}"
    #         cache.set(key, rate, 60 * 60 * 12)
    # else:
    #     print("cache hit")

    return get_exchange_rates(currency_to)[currency_from]


class RecurringExpense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    active = models.BooleanField(default=True)
    particulars = models.CharField(unique=True, max_length=256)
    currency = models.CharField(max_length=3)
    period = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(
        BankAccount, on_delete=models.SET_NULL, null=True, blank=True
    )

    @property
    def amount_nzd(self):
        fx_rate = get_exchange_rate(self.currency)
        return float(self.amount) * fx_rate

    @property
    def yearly_impact(self):
        return 12 / self.period * self.amount_nzd

    @property
    def monthly_impact(self):
        return self.yearly_impact / 12

    @property
    def daily_impact(self):
        return self.yearly_impact / 365.24

    def __str__(self):
        return "RecurringExpense({})".format(
            str(
                {
                    "id": self.id,
                    "active": self.active,
                    "particulars": self.particulars,
                    "amount": self.amount,
                    "currency": self.currency,
                    "period": self.period,
                    "amount_nzd": self.amount_nzd,
                }
            )
        )
