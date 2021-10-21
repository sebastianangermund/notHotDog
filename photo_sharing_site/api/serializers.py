from rest_framework import serializers
from django.contrib.auth.models import User
from photo_sharing_site.photos.models import Photo


class UserSerializer(serializers.ModelSerializer):
    photos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Photo.objects.all(),
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'photos')


class PhotoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Photo
        fields = ['photo', 'title', 'owner', 'description', 'id', 'flagged']
        read_only_fields = ['photo']


class PhotoFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['photo']


class FlaggedTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['flagged']
