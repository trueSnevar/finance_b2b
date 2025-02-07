from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Wallet, Transaction


class TransactionModelTest(TestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(label="Test Wallet", balance=Decimal('100.0'))

    def test_create_positive_transaction(self):
        _ = Transaction.objects.create(wallet=self.wallet, txid="tx1", amount=Decimal('50.0'))
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal('150.0'))

    def test_create_negative_transaction_valid(self):
        _ = Transaction.objects.create(wallet=self.wallet, txid="tx2", amount=Decimal('-50.0'))
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal('50.0'))

    def test_create_negative_transaction_invalid(self):
        with self.assertRaises(ValidationError):
            Transaction.objects.create(wallet=self.wallet, txid="tx3", amount=Decimal('-150.0'))
