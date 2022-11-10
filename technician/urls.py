from django.urls import path, include
from rest_framework.routers import DefaultRouter

from technician.views import (TechnicianRegisterView, TechnicianLoginView, TechnicianView, TechnicianSpecializationView,
                              TechnicianFeedbackView,)


router = DefaultRouter()

router.register("register", TechnicianRegisterView, basename="technician-registration")
router.register("login", TechnicianLoginView, basename="technician-login")
router.register("details", TechnicianView, basename="technician-details")
router.register("specializations",TechnicianSpecializationView, basename="technician-specialization")
router.register("feedback", TechnicianFeedbackView, basename="technician-feedback")


urlpatterns = [
    path('', include(router.urls)),
]