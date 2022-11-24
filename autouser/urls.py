from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwtviews

from autouser.views import (AutoUserRegistration, AutoUserLogin, TechnicianListingsView, FavouriteTechnicianView,
                            AutoUserView, TechnicianBookingView, FeedbackView)
from technician.views import (SpecializationsView,)

router = DefaultRouter()

router.register("register", AutoUserRegistration, basename="autouser-registration")
router.register("login", AutoUserLogin, basename="autouser-login")
router.register("account", AutoUserView, basename="autouser-account")
router.register("technician-listing", TechnicianListingsView, basename="technician-listings")
router.register('technician-specializations', SpecializationsView, basename="tech-specialization")
router.register("favourites", FavouriteTechnicianView, basename="favourite-technician")
router.register("bookings", TechnicianBookingView, basename="autouser-bookings")
router.register("reviews", FeedbackView, basename="reviews")

urlpatterns = [
    path('', include(router.urls)),
    path('token-refresh', jwtviews.TokenRefreshView.as_view(), name="autouser-token-refresh")
]
