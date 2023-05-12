from django_filters import rest_framework as filters

from core.models import Title


class TitlesFilter(filters.FilterSet):
    category = filters.CharFilter(
        field_name="category__slag",
        lookup_expr="icontains"
    )
    name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )
    genre = filters.CharFilter(
        field_name="genre__slug",
        lookup_expr="icontains"
    )

class Meta:
    model = Title
    fields = "__all__"
