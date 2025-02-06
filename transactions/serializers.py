from rest_framework_json_api import serializers
from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'label', 'balance')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'wallet', 'txid', 'amount')

    def validate(self, data):
        wallet = data.get('wallet', self.instance.wallet if self.instance else None)
        amount = data.get('amount', self.instance.amount if self.instance else None)
        if wallet and amount is not None:
            if wallet.balance + amount < 0:
                raise serializers.ValidationError("Wallet balance cannot be negative.")
        return data
