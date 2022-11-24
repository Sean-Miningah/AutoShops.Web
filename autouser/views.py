from datetime import datetime
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet
from rest_framework.mixins import (CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .models import AutoUserFavourite, AutoUser
from .serializers import RegisterAutoUserSerializer, AutoUserSerializer, AutoUserFavouritesSerializer
from technician.serializers import TechnicianDetailsSerializer, AutoUserBookingsSerializer, TechnicianReviews
from technician.models import TechnicianDetails, Bookings, Specialization, TechnicianSpecializations, ShopFeedbackRating


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

        serializer = AutoUserSerializer(user, context={'request': request})

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

    def get_queryset(self):
        user = self.request.user
        queryset = TechnicianDetails.objects.filter().exclude(autouser=user)
        specialist = self.request.query_params.get('specialization')
        if specialist is not None:
            specialization = Specialization.objects.get(id=specialist)
            tech_specialist = TechnicianSpecializations.objects.filter(specialization=specialization)
            queryset = queryset.filter(id__in=tech_specialist)
        return queryset


class FavouriteTechnicianView(GenericViewSet,
                              CreateModelMixin,
                              ListModelMixin,
                              DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = AutoUserFavouritesSerializer

    def get_queryset(self):
        user = self.request.user
        return AutoUserFavourite.objects.filter(auto_user=user)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        technician = TechnicianDetails.objects.get(id=request.data['technician'])
        if not AutoUserFavourite.objects.filter(auto_user=user, technician=technician.autouser).exists():
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
        else:
            return Response(
                {
                    "message": "Technician already favoured!"
                }
            )

    def list(self, request, *args, **kwargs):
        user = self.request.user
        technicians = AutoUserFavourite.objects.filter(auto_user=user)
        tech = []
        for technician in technicians:
            tech.append(TechnicianDetails.objects.get(autouser=technician.technician.values_list('id', flat=True)[0]))
        # serializer = AutoUserFavouritesSerializer(technicians, many=True)
        serial = TechnicianDetailsSerializer(tech, many=True, context={'request': request})
        return Response(
            serial.data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = self.request.user
        technician = TechnicianDetails.objects.get(id=pk)
        AutoUserFavourite.objects.filter(auto_user=user, technician=technician.autouser).delete()
        return Response(
            {
                "message": "Deleted Successfully"
            },
            status=status.HTTP_200_OK,
        )


class TechnicianBookingView(GenericViewSet,
                            CreateModelMixin,
                            ListModelMixin,
                            UpdateModelMixin,
                            RetrieveModelMixin, DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = AutoUserBookingsSerializer

    def get_queryset(self):
        auto_user = self.request.user
        return Bookings.objects.filter(auto_user=auto_user)

    def create(self, request, *args, **kwargs):
        auto_user = self.request.user
        user = AutoUser.objects.get(id=auto_user.id)
        data = self.request.data
        booking = Bookings.objects.create(
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            time=datetime.strptime(data['time'], '%H:%M').time(),
            auto_user=self.request.user,
            technician=TechnicianDetails.objects.get(id=data['technician']),
            autouser_description=data['autouser_description']
        )

        serializer = self.get_serializer(booking)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class FeedbackView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TechnicianReviews

    def get_queryset(self):
        te = self.request.query_params.get('technician')
        technician = TechnicianDetails.objects.get(id=te)
        return ShopFeedbackRating.objects.filter(technician=technician)

    def create(self, request, *args, **kwargs):
        auto_user = self.request.user
        user = AutoUser.objects.get(id=auto_user.id)
        technician = TechnicianDetails.objects.get(id=self.request.data['technician'])
        rating = ShopFeedbackRating.objects.create(
            autouser=user,
            technician=technician,
            description=self.request.data['description'],
            rating=self.request.data['rating']
        )

        serializer = TechnicianReviews(rating, context={'request': request})

        return Response({
            "data": serializer.data
        })