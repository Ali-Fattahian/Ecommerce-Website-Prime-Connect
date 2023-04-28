from rest_framework import generics, permissions, status, filters
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from core.serializers import UserSerializer, UserSerializerWithToken, MessageSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from core.models import Message


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
    if request.user.is_staff == False:
        return Response({'detail': 'You don\'nt have the permission for this request'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.user.id != user.id and user.is_staff:
        return Response({'detail': 'You can\'nt edit an admin level account'}, status=status.HTTP_401_UNAUTHORIZED)

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

    if request.data.get('password'):
        sent_password = request.data['password']

    if request.user == user and sent_password != '': # Only allowed to change your own password
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


class GetAdminUsers(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return get_user_model().objects.filter(
            is_staff=True).order_by('-join_date').exclude(email=self.request.user.email)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def send_message(request):
    try:
        recipient = get_object_or_404(
            get_user_model(), id=request.data['recipient'])
        if recipient.is_staff == False:
            return Response({'You can only send messasges to admins'}, status=status.HTTP_400_BAD_REQUEST)
        content = request.data['content']
        message = Message.objects.create(
            sender=request.user, recipient=recipient, content=content)
    except:
        return Response({'detail': 'Please fill all the fields'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class AllReceivedMessages(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user).order_by('-createdAt')


class AllSentMessages(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user).order_by('-createdAt')


class ReceivedMessageDetail(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        pk = self.kwargs.get('pk')
        message = get_object_or_404(Message, pk=pk)
        if self.request.user == message.recipient:
            message.isRead = True
            message.save()
            return message


class SentMessageDetail(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        pk = self.kwargs.get('pk')
        message = get_object_or_404(Message, pk=pk)
        if self.request.user == message.recipient:
            message.isRead = True
            message.save()
            return message
        return message


@api_view(['PUT'])
@permission_classes([permissions.IsAdminUser])
def change_message_status(request, pk):
    try:
        message = get_object_or_404(Message, pk=pk)
        if request.user == message.recipient:
            isRead = request.data['isRead']
            message.isRead = isRead
            message.save()
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'You don\'nt have the permission for this action'}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({'detail': 'An error occured while processing your request'}, status=status.HTTP_400_BAD_REQUEST)
