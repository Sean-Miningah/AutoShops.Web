from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .models import AutoUserFavourite, AutoUser
from .serializers import RegisterAutoUserSerializer, AutoUserSerializer, AutoUserFavouritesSerializer
from technician.serializers import TechnicianDetailsSerializer
from technician.models import TechnicianDetails


class AutoUserRegistration(GenericViewSet, CreateModelMixin):
    serializer_class = RegisterAutoUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({
            "user": serializer.data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class AutoUserLogin(ViewSet, CreateModelMixin):

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            res = {
                "message": "Invalid username/password",
            }
            return Response(res, status.HTTP_401_UNAUTHORIZED)

        serializer = AutoUserSerializer(user)

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        res = {
            "data": serializer.data,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        return Response(res, status.HTTP_201_CREATED)


class AutoUserView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AutoUserSerializer

    def get_queryset(self):
        user = self.request.user
        return AutoUser.objects.filter(id=user.id)


class TechnicianListingsView(GenericViewSet, ListModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = TechnicianDetailsSerializer
    queryset = TechnicianDetails.objects.all()


class FavouriteTechnicianView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AutoUserFavouritesSerializer

    def get_queryset(self):
        user = self.request.user
        return AutoUserFavourite.objects.filter(auto_user=user)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        technician = TechnicianDetails.objects.get(id=request.data['technician'])
        favourite = AutoUserFavourite()
        favourite.save()
        favourite.auto_user.add(user)
        favourite.technician.add(technician.autouser)
        serializer = AutoUserFavouritesSerializer(instance=favourite)
        return Response(
            {
                "favourites": serializer.data,
                "message": "Added Favourites"
            },
            status=status.HTTP_201_CREATED,
        )
