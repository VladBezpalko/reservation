from django.conf.urls import url
from django.contrib import admin
from reservation.views import RoomReservationViewSet, UsersViewSet

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

router = DefaultRouter()
router.register(r'reservation', RoomReservationViewSet)
router.register(r'users', UsersViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', views.obtain_auth_token),
]

urlpatterns += router.urls
