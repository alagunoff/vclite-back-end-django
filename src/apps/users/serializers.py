from collections import OrderedDict
from rest_framework import serializers

from .models import User as UserModel


class User(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'password', 'first_name', 'last_name',
                  'avatar', 'creation_date', 'is_admin', 'last_login']

    def to_representation(self, instance):
        result = super().to_representation(instance)

        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])
