from rest_framework import viewsets, filters
from rest_framework_json_api.pagination import JsonApiPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer


class WalletPagination(JsonApiPageNumberPagination):
    page_size = 5


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    pagination_class = WalletPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['label']
    ordering_fields = ['id', 'label', 'balance']
    search_fields = ['label']


class TransactionPagination(JsonApiPageNumberPagination):
    page_size = 5


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = TransactionPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['wallet', 'txid']
    ordering_fields = ['id', 'amount']
    search_fields = ['txid']
