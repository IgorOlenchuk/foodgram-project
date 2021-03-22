import os

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from dotenv import load_dotenv
from rest_framework import permissions, status, viewsets, mixins
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdminOnly
from .serializers import (ConfirmationCodeSerializer, PutchUserSerializer,
                          UserCreationSerializer, UserSerializer)

FROM_EMAIL = os.getenv('FROM_EMAIL')

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAdminOnly,)

    @action(detail=False, methods=['get', 'patch'], url_path='me',
            permission_classes=[permissions.IsAuthenticated, ])
    def get_itself(self, request):
        instance = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = PutchUserSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CodeGenerationViewSet(mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = UserCreationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        email = request.data['email']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(
            email=email,
            defaults={'email': email, 'username': email.partition("@")[0]}
            )
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        if created:
            user.password = confirmation_code
        user.save(update_fields=['confirmation_code', 'password'])
        load_dotenv()
        send_mail(
            subject='Confirmation code',
            message=f'Confirmation code: {confirmation_code}',
            from_email=FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenGenerationViewSet(mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = ConfirmationCodeSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        recived_conf_code = request.data['confirmation_code']
        user = get_object_or_404(User, email=email)
        confirmation_code = default_token_generator.make_token(user)
        
        if recived_conf_code == confirmation_code:
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Неверный код подтверждения!'}, 
                        status=status.HTTP_400_BAD_REQUEST)
