from rest_framework.serializers import ModelSerializer

from ..models.category import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

    def get_fields(self):
        fields = super().get_fields()
        fields['subcategories'] = CategorySerializer(
            many=True, read_only=True)

        return fields
