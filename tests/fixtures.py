import pytest

@pytest.fixture
@pytest.mark.django_db
def access_token(client, django_user_model):
    username = "test_user"
    password = "test_passwd"
    django_user_model.objects.create(username=username, password=password, role='admin')
    response = client.post("/user/token/", {"username": username, "password": password})
    return response.data.get("access")


@pytest.fixture
@pytest.mark.django_db
def user_with_access_token(client, django_user_model):
    username = "test_user"
    password = "test_passwd"
    test_user = django_user_model.objects.create(username=username, password=password, role='admin')
    response = client.post("/user/token/", {"username": username, "password": password})
    return test_user, response.data.get("access")
