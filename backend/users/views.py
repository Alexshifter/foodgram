from django.core.exceptions import PermissionDenied
from djoser.serializers import SetPasswordSerializer
from rest_framework import decorators, status, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.paginators import FoodgramPaginator
from users.models import Following, NewUser
from .serializers import (AvatarSerializer, FollowingSerializer,
                          NewUserCreateSerializer, NewUserGetSerializer)


class NewUserViewSet(viewsets.ModelViewSet):

    """Вьюсет для работы с пользователем."""

    model = NewUser
    queryset = NewUser.objects.all()
    serializer_classes = {
        'retrieve': NewUserGetSerializer,
        'list': NewUserGetSerializer,
        'create': NewUserCreateSerializer,
        'me': NewUserGetSerializer,
        'set_or_delete_avatar': AvatarSerializer,
        'subscriptions': FollowingSerializer,
        'subscribe': FollowingSerializer,
    }

    serializer_class = NewUserGetSerializer
    pagination_class = FoodgramPaginator

    def get_permissions(self):

        """Установка пермишенов."""

        if self.action in ['destroy']:
            return [IsAdminUser(),]
        elif self.action in ['create', 'list', 'retrieve']:
            return [AllowAny(),]
        return [IsAuthenticated(),]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    @decorators.action(
        methods=['GET'],
        detail=False,)
    def me(self, request):

        """Профиль пользователя."""

        current_user = request.user
        serializer = self.get_serializer(current_user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @decorators.action(methods=['POST'],
                       detail=False,
                       )
    def set_password(self, request, *args, **kwargs):

        """Изменение пароля пользователя."""

        serializer = SetPasswordSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):

        """Ограничение на изменение чужих данных."""

        if serializer.instance.user != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    @decorators.action(methods=['PUT', 'DELETE'], detail=False,
                       url_path='me/avatar', url_name='my_avatar',
                       )
    def set_or_delete_avatar(self, request):

        """Добавление/удаление аватара пользователя."""

        current_user = self.request.user
        if request.method == 'DELETE':
            request.data['avatar'] = None
            serializer = self.get_serializer(data=request.data,
                                             instance=current_user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = AvatarSerializer(data=request.data,
                                      instance=current_user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @decorators.action(methods=['GET'], detail=False,
                       url_path='subscriptions',
                       )
    def subscriptions(self, request):

        """Список подписок пользователя."""

        user_obj = request.user
        qs = user_obj.follower.all()
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page, many=True,
                                         context={'request': request})
        return self.get_paginated_response(serializer.data)

    @decorators.action(methods=['POST', 'DELETE'], detail=True,
                       url_path='subscribe',
                       )
    def subscribe(self, request, pk):

        """Подписка на автора."""

        author_recipes = self.get_object()
        current_user = request.user
        if request.method == 'POST':
            serializer = self.get_serializer(
                data={'following': author_recipes.username},
                context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=current_user)
            return Response(status=status.HTTP_201_CREATED,
                            data=serializer.data)
        unsubscribed_user = Following.objects.filter(user=current_user,
                                                     following=author_recipes)
        if not unsubscribed_user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        unsubscribed_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
