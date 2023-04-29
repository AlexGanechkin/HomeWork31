from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from ads.models import Selection, User
from ads.serializers.ad_serializers import AdSerializer


# ---------------------------------------- берем с разбора --------------------------------
class SelectionSerializer(ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionListSerializer(ModelSerializer):
    owner = SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Selection
        fields = ['owner', 'name']


class SelectionDetailSerializer(ModelSerializer):
    items = AdSerializer(many=True)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(ModelSerializer):
    owner = SlugRelatedField(slug_field='username', queryset=User.objects.all(), required=False)
    # owner = SlugRelatedField(slug_field='username', read_only=True)  - второй вариант

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return super().create(validated_data)

    class Meta:
        model = Selection
        fields = '__all__'


# ---------------------------------------- пытался писать сам --------------------------------
"""
class SelectionCreateSerializer(ModelSerializer):
    location_id = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Selection
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop('location_id', [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        passwd = validated_data.pop("password")
        user = User.objects.create(**validated_data)  # От наставника
        user.set_password(passwd)  # От наставника
        user.save()  # От наставника

        for location_id in self._locations:
            loc_obj, _ = Location.objects.get_or_create(name=location_id)
            user.location_id.add(loc_obj)

        return user
"""
