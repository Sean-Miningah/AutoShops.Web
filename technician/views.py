from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import TechnicianDetails, ShopFeedbackRating, TechnicianSpecializations, Specialization
from .serializers import (RegisterTechnicianSerializer, TechnicianSerializer, TechnicianDetailsSerializer,
                          ShopFeedbackRatingSerializer, TechnicianSpecializationsSerializer, SpecializationSerializer,
                          TechnicianLoginSerializer)


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


class TechnicianLoginView(GenericViewSet, CreateModelMixin):

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            res = {
                "message": "Invalid username/password"
            }
            return Response(res)

        technician = TechnicianDetails.objects.get(autouser=user)
        # serializer = TechnicianSerializer(user, context={'request': request})
        serializer = TechnicianLoginSerializer(technician, context={'request': request})
        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        res = {
            "data": serializer.data,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        return Response(res)


class TechnicianOnBoardingView(GenericViewSet, CreateModelMixin):
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        #     save the technician details
        user = request.user
        specializations = request.data['specializations']
        technician = TechnicianDetails(
            autouser=user,
            lat=request.data['lat'],
            lng=request.data['lng'],
            profile_picture=request.data['profile_pic'],
            shop_description=request.data['shop_description'],
            shop_goal=request.data['shop_goal'],
        )
        technician.save()

        # Save the specializations
        for data in specializations:
            specialization = Specialization.objects.get(id=data)
            specialize = TechnicianSpecializations()
            specialize.save()
            specialize.technician.add(user)
            specialize.specialization.add(specialization)

        return Response(
            {
                "message": "You have successfully registered, Login in to access the application."
            },
            status=status.HTTP_201_CREATED
        )


class TechnicianFeedView(GenericViewSet, CreateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = TechnicianDetailsSerializer

    def get_queryset(self):
        user = self.request.user
        return TechnicianDetails.objects.filter().exclude(autouser=user)


class SpecializationsView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer


class TechnicianView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TechnicianDetails.objects.all()
    serializer_class = TechnicianDetailsSerializer

    def list(self, request, *args, **kwargs):
        pass


class TechnicianSpecializationView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TechnicianSpecializations.objects.all()
    serializer_class = TechnicianSpecializationsSerializer


class TechnicianFeedbackView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ShopFeedbackRating.objects.all()
    serializer_class = ShopFeedbackRatingSerializer
