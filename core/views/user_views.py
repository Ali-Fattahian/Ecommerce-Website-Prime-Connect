from rest_framework import generics, permissions, status, filters
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from core.serializers import UserSerializer, UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class GetUserProfile(generics.RetrieveDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user.id == instance.id or self.request.user.is_staff:
            return super().perform_destroy(instance)
        message = {'detail': 'You don\'nt have the permission for this action'}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_user_profile(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    if request.user.id != user.id or request.user.is_staff == False:
        return Response({'detail': 'You don\'nt have the permission for this request'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = UserSerializerWithToken(user, many=False)

    user.fullname = request.data.get('fullname', user.fullname)
    user.email = request.data.get('email', user.email)

    if request.data['password'] != '':
        user.password = make_password(request.data['password'])

    user.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


class GetUsers(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ('fullname', 'email')
    order_by = ('-id')


@api_view(['POST'])
def register_user(request):
    try:
        data = request.data
        user = get_user_model().objects.create_user(
            email=data['email'], fullname=data['fullname'], password=data['password'], is_active=True)

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)

    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
