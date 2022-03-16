from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from rest_framework.authtoken import views

from api.views import PostViewSet, CommentViewSet, GroupViewSet


router = routers.DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comments")
router.register(r"groups", GroupViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-token-auth/", views.obtain_auth_token),
    path("", include(router.urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
