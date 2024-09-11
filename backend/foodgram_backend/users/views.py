from rest_framework.response import Response
from rest_framework import status, viewsets
from users.models import NewUser, Following
from .serializers import (NewUserCreateSerializer,
                          AvatarSerializer,
                          NewUserGetSerializer,
                          FollowingSerializer)
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import (decorators, status, viewsets)
from djoser.serializers import SetPasswordSerializer
from django.core.exceptions import PermissionDenied 
from api.paginators import FoodgramPaginator


class NewUserViewSet(viewsets.ModelViewSet):
    model = NewUser
    queryset = NewUser.objects.all()
    serializer_classes = {
        'retrieve': NewUserGetSerializer,
        'list': NewUserGetSerializer,
        'create': NewUserCreateSerializer,
        'me': NewUserGetSerializer,
      #  'subscriptions': FollowingSerializer,

    }

    serializer_class = NewUserGetSerializer
    permission_classes = (AllowAny,)
    pagination_class = FoodgramPaginator

    def get_permissions(self):
        if self.action in ['destroy']:
            return [IsAdminUser(),]
        elif self.action in ['create', 'list', 'retrieve']:
            return[AllowAny(),]

        return [IsAuthenticated(),]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    @decorators.action(
         methods=['GET'],
         detail=False,
         permission_classes=(IsAuthenticated,))

    def me(self, request):
        current_user = request.user
        serializer = self.get_serializer(current_user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @decorators.action(methods=['POST'], detail=False, permission_classes=(IsAuthenticated,))
    def set_password(self, request, *args, **kwargs):

        serializer = SetPasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer): 
        if serializer.instance.user != self.request.user: 
            raise PermissionDenied('Изменение чужого контента запрещено!') 
        super().perform_update(serializer)
    
    @decorators.action(methods=['PUT', 'DELETE'], detail=False, 
                       url_path='me/avatar', url_name='my_avatar', 
                       permission_classes = [IsAuthenticated,])
    def set_or_delete_avatar(self, request):
        current_user = self.request.user
        if request.method == 'DELETE':
            request.data['avatar'] = None
            serializer = AvatarSerializer(data=request.data, instance=current_user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = AvatarSerializer(data = request.data, instance=current_user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    @decorators.action(methods=['GET'], detail=False,
                       url_path='subscriptions',
                       permission_classes=[IsAuthenticated,],
                       pagination_class=FoodgramPaginator)

    def subscriptions(self, request):
        print(request.path)

        user_obj = request.user
        qs = user_obj.follower.all()
        page = self.paginate_queryset(qs)
#        self.get_paginated_response

        serializer = FollowingSerializer(page, many=True, context = {'request': request})
        return self.get_paginated_response(serializer.data)

    @decorators.action(methods=['POST', 'DELETE'], detail=True,
                       url_path='subscribe', 
                       permission_classes = [IsAuthenticated,])
    
    def subscribe(self, request, pk):
        author_recipes = self.get_object()
        current_user = request.user 
        if request.method =='POST':
            serializer = FollowingSerializer(data = {'following': author_recipes.username}, context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save(user = current_user)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        unsubscribed_user = Following.objects.filter(user=current_user, following=author_recipes)
        if not unsubscribed_user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        unsubscribed_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
