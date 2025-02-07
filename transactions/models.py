from decimal import Decimal
from django.db import models, transaction as db_transaction
from django.core.exceptions import ValidationError


class Wallet(models.Model):
    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=38, decimal_places=18, default=Decimal('0.0'))

    def __str__(self):
        return self.label


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=38, decimal_places=18)

    def clean(self):
        # Wallet balance should never be negative.
        new_balance = self.wallet.balance + self.amount
        if new_balance < 0:
            raise ValidationError("Wallet balance cannot be negative.")

    def save(self, *args, **kwargs):
        with db_transaction.atomic():
            # If updating an existing transaction, adjust for the difference in amount.
            if self.pk:
                orig = Transaction.objects.get(pk=self.pk)
                diff = self.amount - orig.amount
            else:
                diff = self.amount
            new_balance = self.wallet.balance + diff
            if new_balance < 0:
                raise ValidationError("Wallet balance cannot be negative.")
            # Update wallet balance
            self.wallet.balance = new_balance
            self.wallet.save()
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with db_transaction.atomic():
            new_balance = self.wallet.balance - self.amount
            if new_balance < 0:
                raise ValidationError("Wallet balance cannot be negative after deleting this transaction.")
            self.wallet.balance = new_balance
            self.wallet.save()
            super().delete(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['txid']),
            models.Index(fields=['wallet']),
        ]
