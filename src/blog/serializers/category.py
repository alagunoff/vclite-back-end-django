from rest_framework.serializers import ModelSerializer

from ..models.category import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ('parent_category',)

    def get_fields(self):
        fields = super().get_fields()
        fields['subcategories'] = CategorySerializer(
            many=True, read_only=True)

        return fields
