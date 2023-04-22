from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from ads.models import Publication, User, Category
from ads.serializers.serializers import UserSerializer, UserDetailSerializer


class AdSerializer(ModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'


class AdListSerializer(ModelSerializer):
    author_id = SlugRelatedField(slug_field='username', queryset=User.objects.all())
    category_id = SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Publication
        fields = '__all__'


class AdDetailSerializer(ModelSerializer):
    author_id = UserDetailSerializer()
    category_id = SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Publication
        fields = '__all__'