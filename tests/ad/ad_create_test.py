import pytest
from rest_framework import status


@pytest.mark.django_db
def test_ad_create(client, user, category, access_token):
    data = {
        "author_id": user.username,
        "category_id": category.name,
        "name": "Super Chair",
        "price": 100
    }

    expected_data = {
        "id": 1,
        "author_id": user.username,
        "category_id": category.name,
        "name": "Super Chair",
        "price": 100,
        "is_published": False,
        "description": None,
        "image": None
    }
    response = client.post("/ad/", data=data, HTTP_AUTHORIZATION=f"Bearer {access_token}")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_data
