from rest_framework import serializers

from ..models.category import Category as CategoryModel


class Category(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['id', 'category']

    def to_representation(self, instance):
        category = super().to_representation(instance)
        subcategories = instance.subcategories.all()

        if subcategories.exists():
            category['subcategories'] = Category(
                subcategories, many=True).data

        return category
