from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import Count
from .models import Availability
from .serializers import AvailabilitySerializer
from django.contrib.auth import get_user_model
import csv

User = get_user_model()

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.select_related('user').all()
    serializer_class = AvailabilitySerializer

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[])
    def summary_by_date(self, request):
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        user_ids = request.query_params.get('user_ids')
        qs = Availability.objects.filter(status=Availability.STATUS_AVAILABLE)
        if start and end:
            qs = qs.filter(date__range=[start, end])
        if user_ids:
            ids = [int(x) for x in user_ids.split(',') if x.strip().isdigit()]
            qs = qs.filter(user_id__in=ids)
            group_size = len(ids)
        else:
            group_size = User.objects.count()
        aggregated = qs.values('date').annotate(available_count=Count('user', distinct=True)).order_by('date')
        data = [{'date': a['date'], 'available_count': a['available_count'], 'group_size': group_size,
                 'percentage': (a['available_count']/group_size*100 if group_size else 0)} for a in aggregated]
        return Response(data)

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        qs = self.get_queryset()
        if start and end:
            qs = qs.filter(date__range=[start, end])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=availability.csv'
        writer = csv.writer(response)
        writer.writerow(['Date','Time Slot','User ID','Username','Status','Note'])
        for a in qs.order_by('date').all():
            writer.writerow([a.date, a.time_slot, a.user.id, a.user.username, a.status, a.note or ''])
        return response
