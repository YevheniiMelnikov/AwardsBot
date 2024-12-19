from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.awards.views import UserViewSet, NominationViewSet, CandidateViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"nominations", NominationViewSet)
router.register(r"candidates", CandidateViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
