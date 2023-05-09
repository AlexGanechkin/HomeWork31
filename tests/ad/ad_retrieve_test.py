import pytest
from rest_framework import status

from ads.serializers.ad_serializers import AdDetailSerializer
from tests.factories import PublicationFactory


@pytest.mark.django_db
def test_ad_retrieve(client, access_token):
    ad = PublicationFactory.create()

    response = client.get(f"/ad/{ad.pk}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.get(f"/ad/{ad.pk}", HTTP_AUTHORIZATION=f"Bearer {access_token}")

    assert response.status_code == status.HTTP_200_OK
    assert response.data == AdDetailSerializer(ad).data
