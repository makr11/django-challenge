from django.contrib.auth.models import User, Group
from app.models import GreatProduct, UserRatings
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class GreatProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GreatProduct
        fields = ['id', 'name', 'rating', 'price', 'updated_at']


class UserRatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRatings
        fields = ['id', 'user', 'product', 'rating', 'created_at']
