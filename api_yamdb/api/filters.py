import django_filters

from reviews.models import Title


class TitlesFilter(django_filters.FilterSet):
    """
    Фильтрует объекты модели Title по категории, жанру, году и имени.
    """

    category = django_filters.CharFilter(field_name='category__slug')
    genres = django_filters.CharFilter(field_name='genres__slug')
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('category', 'genres', 'year', 'name')
