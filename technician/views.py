from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import TechnicianDetails, ShopFeedbackRating, TechnicianSpecializations
from .serializers import (RegisterTechnicianSerializer, TechnicianSerializer, TechnicianDetailsSerializer,
                          ShopFeedbackRatingSerializer, TechnicianSpecializationsSerializer)


class TechnicianRegisterView(GenericViewSet, CreateModelMixin):
    serializer_class = RegisterTechnicianSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({
            "user": serializer.data,
            "message": "Successful Technician Account Creation.  Now perform Login to get your token.",
        },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    pass


class TechnicianLoginView(ModelViewSet):
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            res = {
                "message": "Invalid username/password"
            }
            return Response(res)

        serializer = TechnicianSerializer(user)

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        res = {
            "data": serializer.data,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        return Response(res)

    pass


class TechnicianView(ModelViewSet):
    http_method_names = ['head', 'get']
    permission_classes = (IsAuthenticated,)
    queryset = TechnicianDetails.objects.all()
    serializer_class = TechnicianDetailsSerializer

    def list(self, request, *args, **kwargs):
        pass


class TechnicianSpecializationView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = TechnicianSpecializations.objects.all()
    serializer_class = TechnicianSpecializationsSerializer


class TechnicianFeedbackView(ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    permission_classes = (IsAuthenticated,)
    queryset = ShopFeedbackRating.objects.all()
    serializer_class = ShopFeedbackRatingSerializer
