from rest_framework import decorators, filters
import django_filters
from django_filters import FilterSet, MultipleChoiceFilter
from .models import Recipe, Tag, Ingredient
from django.db.models import Count


class IngredientsSearchFilter(filters.SearchFilter):
    search_param='name'


class RecipesSearchFilter(django_filters.FilterSet):

    QUERY_PARAM = ('0', '1',)

    author = django_filters.CharFilter()
    tags = django_filters.ModelMultipleChoiceFilter(field_name = 'tags__slug',  
                                                    to_field_name = 'slug',
                                                    queryset = Tag.objects.all())
    is_favorited = django_filters.CharFilter(method='get_favorite_recipes')
    is_in_shopping_cart = django_filters.CharFilter(method='get_recipes_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def get_favorite_recipes(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            if value == self.QUERY_PARAM[1]:
                return queryset.filter(favorite__user=self.request.user)
            elif value==self.QUERY_PARAM[0]:
                return queryset.exclude(favorite__user=self.request.user)
        return queryset

    def get_recipes_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value == self.QUERY_PARAM[1]:
                return queryset.filter(shopping_cart__user=self.request.user)
            elif value == self.QUERY_PARAM[0]:
                return queryset.exclude(shopping_cart__user=self.request.user)
        return queryset
