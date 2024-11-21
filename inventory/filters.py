import django_filters
from thefuzz import fuzz
from .models import Food

class FoodFilter(django_filters.FilterSet):
    fuzzy_search = django_filters.CharFilter(method='filter_fuzzy_search')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Food
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(brand__icontains=value | Q(category__name__icontains=value))
        )

    def filter_fuzzy_search(self, queryset, name, value):
        import pdb; pdb.set_trace()
        # Annotate each food item with its fuzzy match score
        annotated_queryset = queryset.annotate(
            fuzzy_score=Cast(Value(0), IntegerField())
        )

        # Update the fuzzy_score for each item
        for food in annotated_queryset:
            food.fuzzy_score = fuzz.ratio(food.name, value)

        # Sort the queryset by the fuzzy_score in descending order
        sorted_queryset = sorted(
            annotated_queryset,
            key=lambda food: food.fuzzy_score,
            reverse=True
        )

        # Extract the IDs of the sorted items
        sorted_ids = [food.id for food in sorted_queryset]

        # Return the queryset ordered by the sorted IDs
        return queryset.filter(id__in=sorted_ids).order_by(
            models.Case(
                *[models.When(id=id, then=pos) for pos, id in enumerate(sorted_ids)]
            )
        )
