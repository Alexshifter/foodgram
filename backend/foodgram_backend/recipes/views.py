import io

from api.paginators import FoodgramPaginator
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import decorators, mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientsSearchFilter, RecipesSearchFilter
from .models import Favorite, Ingredient, Recipe, Shopping_cart, ShortLink, Tag
from .permissions import IsOwnerOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeGetSerializer,
                          ShoppingCartSerializer, ShortLinkSerializer,
                          TagSerializer)
from .shopping_cart import create_pdf_template


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    model = Tag
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    model = Ingredient
    permission_classes = (AllowAny,)
    queryset = Ingredient.objects.all()
    filter_backends = (IngredientsSearchFilter,)
    search_fields = ('^name',)


class ShortLinkView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ShortLink.objects.all()

    def redirect_to_original_uri(self, request, pk=None, short_code_path=None):
        obj_with_paths = get_object_or_404(ShortLink,
                                           short_code_path=short_code_path)
        original_uri = request.build_absolute_uri(obj_with_paths.original_path)
        return redirect(original_uri)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_classes = {
        'retrieve': RecipeGetSerializer,
        'list': RecipeGetSerializer,
        'create': RecipeCreateSerializer,
        'partial_update': RecipeCreateSerializer,
        'destroy': RecipeCreateSerializer,
        'favorite': FavoriteSerializer,
        'get_link': ShortLinkSerializer,
        'shopping_cart': ShoppingCartSerializer,
    }
    model = Recipe
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = FoodgramPaginator
    filter_backends = (
        DjangoFilterBackend,)
    filterset_class = RecipesSearchFilter
    filterset_fields = ('is_favorited',)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @decorators.action(
        detail=True,
        methods=('GET',),
        permission_classes=[AllowAny,],
        url_path='get-link')
    def get_link(self, request, pk):
        instance = self.get_object()
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance,
                                         context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post_delete_recipes_for_fav_and_shop_cart(self, request, pk, Model):
        instance = self.get_object()
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'DELETE':
            obj = Model.objects.filter(recipe=instance.id,
                                       user=request.user.id)
            if obj:
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data={'user': request.user.id,
                                               'recipe': instance.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @decorators.action(
        detail=True,
        methods=('POST', 'DELETE'),
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        return self.post_delete_recipes_for_fav_and_shop_cart(
            request, pk, Favorite
        )

    @decorators.action(
        detail=True,
        methods=('POST', 'DELETE'),
        permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.post_delete_recipes_for_fav_and_shop_cart(
            request, pk, Shopping_cart
        )

    @decorators.action(
        detail=False,
        methods=('GET',),
        permission_classes=[IsAuthenticated],
        url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        current_user = self.request.user
        queryset = Recipe.objects.filter(
            shopping_cart__user=current_user).values(
                'ingredients__name', 'ingredients__measurement_unit'
        ).annotate(total=Sum('ingredients_in_recipe__amount'))
        buffer = io.BytesIO()
        return FileResponse(create_pdf_template(buffer, queryset,
                            current_user.username), as_attachment=True,
                            filename="shopping_cart.pdf")
