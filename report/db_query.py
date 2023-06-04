from eco.models import Reports
from .serializers import ReportCreateSerializer
from django.db import transaction

@transaction.atomic
def create_report():
    pass