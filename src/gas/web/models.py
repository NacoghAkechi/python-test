from django.db import models


class CustomerRecord(models.Model):
    email = models.EmailField()
    web_statement = models.BooleanField()


class BillRecord(models.Model):
    customer = models.ForeignKey(CustomerRecord, on_delete=models.PROTECT)
    usage = models.IntegerField()
    amount = models.IntegerField()
