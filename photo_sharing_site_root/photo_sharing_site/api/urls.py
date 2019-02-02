from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'photos', views.PhotoViewSet)


urlpatterns = [
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    path(r'', include(router.urls)),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]
