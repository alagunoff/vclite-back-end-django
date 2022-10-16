from rest_framework import serializers

from shared.utils import refine_serialized_model

from .models import User as UserModel


class User(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'password', 'first_name', 'last_name',
                  'avatar', 'creation_date', 'is_admin']

    def to_representation(self, user):
        return refine_serialized_model(super().to_representation(user))
