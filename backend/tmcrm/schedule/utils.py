from rest_framework.response import Response
from collections import defaultdict


def _grouped_response(self, field_name=None, serializer_class=None):
    schedules = self.get_queryset().exclude(**{f"{field_name}__isnull": True})
    filterset = self.filterset_class(self.request.GET, queryset=schedules)
    schedules = filterset.qs
    
    grouped = defaultdict(list)
    for schedule in schedules:
        key = getattr(schedule, field_name)
        grouped[key].append(schedule)
    
    response_data = []
    for key_obj, schedule_list in grouped.items():
        serializer = serializer_class(instance={
            f'{field_name}': key_obj,
                'schedules': schedule_list
        })
        response_data.append(serializer.data)
        
    return Response(response_data)