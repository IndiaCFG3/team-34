from django.urls import path, include
from .views import (
    PingView,
    MobilizerLoginView,
    MobilizerLogoutView,
    MobilizerSignupView,
    MobilizerDetailsView,
    OperationManagerLoginView,
    OperationManagerLogoutView,
    OperationManagerDetailsView,
    OperationManagerSignupView,
    GetMobilizerView,
    EventView,
    GetDataMobiliser,
    StudentsDetails,
    WhatsappStudentsDetails
)
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path("ping/", PingView.as_view()),
    path("mob/login/", MobilizerLoginView.as_view()),
    path("mob/signup/", MobilizerSignupView.as_view()),
    path("mob/logout/", MobilizerLogoutView.as_view()),
    path("mob/detials/", MobilizerDetailsView.as_view()),
    path("om/login/", OperationManagerLoginView.as_view()),
    path("om/signup/", OperationManagerSignupView.as_view()),
    path("om/logout/", OperationManagerLogoutView.as_view()),
    path("om/detials/", OperationManagerDetailsView.as_view()),
    path("om/getMob/", GetMobilizerView.as_view()),
    path("mob/event/", EventView.as_view()),
    path("mob/event/<int:pk>/", EventView.as_view()),
    path("om/data/<int:pk>/", GetDataMobiliser.as_view()),
    path("mob/studentDetails/", StudentsDetails.as_view()),
    path("mob/whatsapp/studentDetails/", WhatsappStudentsDetails.as_view())
]
