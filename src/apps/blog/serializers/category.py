from rest_framework import serializers

from ..models.category import Category as CategoryModel


class Category(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['id', 'category']

    def to_representation(self, category):
        serialized_category = super().to_representation(category)

        subcategories = category.subcategories.all()
        if subcategories.exists():
            serialized_category['subcategories'] = Category(
                subcategories, many=True).data

        return serialized_category
