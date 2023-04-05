from rest_framework import generics, permissions, status, filters
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
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

    # def handle_exception(self, exc):
    #     except
    #     return super().handle_exception(exc)

    def perform_destroy(self, instance):
        if self.request.user.is_staff == False or self.request.user.id != instance.id:
            return Response({'detail': 'You don\'nt have the permission for this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().perform_destroy(instance)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_user_profile(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    if request.user.is_staff == False or request.user.id != user.id:
        return Response({'detail': 'You don\'nt have the permission for this request'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = UserSerializerWithToken(user, many=False)

    fullname = request.data.get('fullname')
    email = request.data.get('email')

    if fullname and len(fullname) > 0:
        user.fullname = fullname
    else:
        return Response({'detail': 'Fullname must not be empty'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_email(email)
    except ValidationError as e:
        return Response({'detail': e}, status=status.HTTP_400_BAD_REQUEST)
    else:
        user.email = email

    if request.data.get('password') and request.data['password'] != '':
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
        validate_email(request.data.get('email'))
    except ValidationError as e:
        return Response({'detail': e}, status=status.HTTP_400_BAD_REQUEST)
    try:
        data = request.data
        user = get_user_model().objects.create_user(
            email=data.get('email'), fullname=data.get('fullname'), password=data.get('password'), is_active=True)

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)

    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
