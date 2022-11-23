from django.urls import path, include
from rest_framework.routers import DefaultRouter

from technician.views import (TechnicianRegisterView, TechnicianLoginView, TechnicianView, TechnicianSpecializationView,
                              TechnicianFeedbackView, TechnicianOnBoardingView, SpecializationsView, TechnicianFeedView,
                              TechnicianBookingsView, BookingReportView, ReviewsReportView)


router = DefaultRouter()
reports = DefaultRouter()

router.register("register", TechnicianRegisterView, basename="technician-registration")
router.register("login", TechnicianLoginView, basename="technician-login")
router.register("details", TechnicianView, basename="technician-details")
router.register("specializations", TechnicianSpecializationView, basename="technician-specialization")
router.register("reviews", TechnicianFeedbackView, basename="technician-feedback")
router.register("onboarding", TechnicianOnBoardingView, basename="technician-onboarding")
router.register("technician-specializations", SpecializationsView, basename="technician-specializations")
router.register("technician-feed", TechnicianFeedView, basename="technician-feed")
router.register("bookings", TechnicianBookingsView, basename="technician-bookings")

reports.register("bookings", BookingReportView, basename="booking-reports")
reports.register('reviews', ReviewsReportView, basename="reviews-reports")

urlpatterns = [
    path('', include(router.urls)),
    path('reports/', include(reports.urls))
]
