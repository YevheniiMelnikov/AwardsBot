from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


from api.awards.views import UserViewSet, NominationViewSet, CandidateViewSet, CandidateNominationViewSet, VoteViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"nominations", NominationViewSet)
router.register(r"candidates", CandidateViewSet)
router.register(r"candidatenominations", CandidateNominationViewSet)
router.register(r"votes", VoteViewSet)

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
