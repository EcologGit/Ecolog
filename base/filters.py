from rest_framework.filters import BaseFilterBackend, OrderingFilter
from django.db.models import Count, F


class OrderingFilterWithFunction(OrderingFilter):
    """
    Работает также как и OrderingFilter, но в ordering_fields необходимо засунуть словарь вида:
    поле сортировки :функция, которая будет создавать новое поле в запросе или прописать функцию, которая просто возвращает x,
    если необходимое поле в запросе уже есть, например ordering_fields = {
        "report_count": lambda x: x.annotate(
                    report_count=Count('reports')
                ),
    При этом вновь созданное поле должно называться, как и ключ в словаре!
    }
    """

    @classmethod
    def get_ordering_function(cls, order_field):
        return cls.ordering_fields[order_field[1:]] if order_field.startswith('-') else cls.ordering_fields[order_field]


    @classmethod
    def check_type_ordering_fields(cls):
        if not isinstance(cls.ordering_fields, dict):
            raise TypeError("Поле ordering_fields должно быть словарём!")
        for val in cls.ordering_fields.values():
            if not callable(val):
                raise TypeError(
                    "В ordering_fields значениями словаря могут выступать только функции!"
                )

    @classmethod
    def use_function_from_ordering_fields_on_queryset(cls, queryset, ordering):
        if ordering:     
            for order_field in ordering:
                query_func = cls.get_ordering_function(order_field)
                queryset = query_func(queryset)
        return queryset

    def filter_queryset(self, request, queryset, view):
        self.check_type_ordering_fields()
        ordering = self.get_ordering(request, queryset, view)
        queryset = self.use_function_from_ordering_fields_on_queryset(
            queryset, ordering
        )

        if ordering:
            return queryset.order_by(*ordering)

        return queryset
