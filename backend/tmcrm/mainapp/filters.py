import django_filters


class DateRangeMixin(django_filters.FilterSet):
    start_date = django_filters.DateFilter(lookup_expr="gte")
    end_date = django_filters.DateFilter(lookup_expr="lte")
    date = django_filters.DateFilter()

    date_field = "date"

    def __init__(
        self,
        data=None,
        queryset=None,
        *,
        request=None,
        prefix=None,
    ):
        super().__init__(data, queryset, request=request, prefix=prefix)
        for key in ('start_date', 'end_date', 'date'):
            self.filters[key].field_name = self.date_field
