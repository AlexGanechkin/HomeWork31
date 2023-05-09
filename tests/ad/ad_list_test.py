import pytest
from rest_framework import status

from ads.serializers.ad_serializers import AdDetailSerializer, AdListSerializer
from tests.factories import PublicationFactory


@pytest.mark.django_db
def test_ad_list(client):
    ad_list = PublicationFactory.create_batch(4)

    response = client.get("/ad/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "count": 4,
        "next": None,
        "previous": None,
        "results": AdListSerializer(ad_list, many=True).data
    }
