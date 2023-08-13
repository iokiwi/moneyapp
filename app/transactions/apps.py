from django.apps import AppConfig
# from django.conf import settings
# import beeline


class TransactionsConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transactions'

    # def ready(self):
    #     beeline.init(
    #         writekey=settings.HONEYCOMB_API_KEY,
    #         dataset=settings.HONEYCOMB_DATASET,
    #         service_name="moneyapp",
    #         debug=False,
    #         send_frequency=1,
    #     )
