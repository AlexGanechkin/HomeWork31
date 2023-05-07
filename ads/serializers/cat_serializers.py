from rest_framework.serializers import ModelSerializer

from ads.models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category
