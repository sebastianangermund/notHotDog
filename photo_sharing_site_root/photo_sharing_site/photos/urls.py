from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views


urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('photo_list/', views.PhotoListView.as_view(), name='photo-list-all'),
    path(
        'photo/<uuid:pk>',
        views.PhotoDetailView.as_view(),
        name='my-photo-detail',
    ),
    path(
        'my_photos/',
        views.UploadedByUserListView.as_view(),
        name='my-photos',
    ),
    path('create_photo/', views.PhotoCreate.as_view(), name='create-photo'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
