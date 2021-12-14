from django.urls import path
from .views import PayableView, TransactionView

urlpatterns = [
    path('unpaid/', PayableView.as_view()),
    path('transaction/', TransactionView.as_view()),
]
