from django.urls import path, include
from rest_framework.routers import DefaultRouter

from technician.views import (TechnicianRegisterView, TechnicianLoginView, TechnicianView, TechnicianSpecializationView,
                              TechnicianFeedbackView, TechnicianOnBoardingView, SpecializationsView, TechnicianFeedView)


router = DefaultRouter()

router.register("register", TechnicianRegisterView, basename="technician-registration")
router.register("login", TechnicianLoginView, basename="technician-login")
router.register("details", TechnicianView, basename="technician-details")
router.register("specializations", TechnicianSpecializationView, basename="technician-specialization")
router.register("feedback", TechnicianFeedbackView, basename="technician-feedback")
router.register("onboarding", TechnicianOnBoardingView, basename="technician-onboarding")
router.register("technician-specializations", SpecializationsView, basename="technician-specializations")
router.register("technician-feed", TechnicianFeedView, basename="technician-feed")

urlpatterns = [
    path('', include(router.urls)),
]
