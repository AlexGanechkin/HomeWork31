import pytest
from rest_framework import status

from tests.factories import PublicationFactory


@pytest.mark.django_db
def test_selection_create(client, user_with_access_token):
    user, access_token = user_with_access_token
    ad_list = PublicationFactory.create_batch(4)

    data = {
        "name": "Тестовая подборка",
        "items": [ad.pk for ad in ad_list]
    }

    expected_data = {
        "id": 1,
        "owner": user.username,
        "name": "Тестовая подборка",
        "items": [ad.pk for ad in ad_list]
    }
    response = client.post("/ad/", data=data, HTTP_AUTHORIZATION=f"Bearer {access_token}")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_data
