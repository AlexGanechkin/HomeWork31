from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, IntegerField

from ads.models import Location, User
from ads.serializers.location_serializers import LocationSerializer


class UserSerializer(serializers.ModelSerializer):
    location_id = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = User
        exclude = ['password']


class UserDetailSerializer(serializers.ModelSerializer):
    location_id = LocationSerializer(many=True)

    class Meta:
        model = User
        exclude = ['password']


# Вариант наставника по агрегации полей
class UserListSerializer(serializers.ModelSerializer):
    #total_ads = SerializerMethodField()

    #def get_total_ads(self, user):
    #    return user.ad_set.filter(is_published=True).count()
    total_ads = IntegerField()

    class Meta:
        model = User
        exclude = ['password']


class UserCreateSerializer(serializers.ModelSerializer):
    location_id = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop('location_id', [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        #user.set_password(user.password)

        for location_id in self._locations:
            loc_obj, _ = Location.objects.get_or_create(name=location_id)
            user.location_id.add(loc_obj)

        #user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    location_id = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop('location_id', [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **validated_data):
        user = super().save()

        if self._locations:
            user.location_id.clear()  # чистим локации перед добавлением новых
            for location_id in self._locations:
                loc_obj, _ = Location.objects.get_or_create(name=location_id)
                user.location_id.add(loc_obj)

        user.set_password(user.password)
        user.save()

        return user