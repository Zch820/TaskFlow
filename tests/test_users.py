import pytest
from django.urls import reverse


# ------ Registration Tests ---------------------------------------------------

@pytest.mark.django_db
def test_registration_success(api_client):
    data = {'email': 'new@new.com', 'password': 'TaskFlow_2026', 'confirm_password': 'TaskFlow_2026'}
    response = api_client.post(reverse('register', kwargs={'version': '1'}), data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_registration_failure_password_match(api_client):
    data = {'email': 'new@new.com', 'password': 'TaskFlow_2026', 'confirm_password': 'TaskFlow'}
    response = api_client.post(reverse('register', kwargs={'version': '1'}), data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_registration_failure_missing_fields(api_client):
    data1 = {'email': '', 'password': 'TaskFlow_2026', 'confirm_password': 'TaskFlow_2026'}
    data2 =  {'email': 'new@new.com', 'password': ''}
    response_missing_email = api_client.post(reverse('register', kwargs={'version': '1'}), data1)
    response_missing_password = api_client.post(reverse('register', kwargs={'version': '1'}), data2)
    assert response_missing_email.status_code == 400
    assert response_missing_password.status_code == 400


@pytest.mark.django_db
def test_registration_failure_existing_user(api_client, user):
    data = {'email': 'user@user.com', 'password': 'TaskFlow_2026', 'confirm_password': 'TaskFlow_2026'}
    response = api_client.post(reverse('register', kwargs={'version': '1'}), data)
    assert response.status_code == 400


# ------ Login Tests ---------------------------------------------------

@pytest.mark.django_db
def test_login_success(api_client, user):
    data = {'email': 'user@user.com', 'password': 'TaskFlow_2026'}
    response = api_client.post(reverse('login', kwargs={'version': '1'}), data,format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_failure_not_existing_user(api_client, user):
    data = {'email': 'not@exist.com', 'password': 'TaskFlow_2026'}
    response = api_client.post(reverse('login', kwargs={'version': '1'}), data)
    assert response.status_code == 401


@pytest.mark.django_db
def test_login_failure_wrong_password(api_client, user):
    data = {'email': 'user@user.com', 'password': 'TaskFlow'}
    response = api_client.post(reverse('login', kwargs={'version': '1'}), data)
    assert response.status_code == 401


@pytest.mark.django_db
def test_login_failure_missing_fields(api_client):
    data1 = {'email': '', 'password': 'TaskFlow_2026'}
    data2 = {'email': 'user@user.com', 'password': ''}
    response_missing_email = api_client.post(reverse('login', kwargs={'version': '1'}), data1)
    response_missing_password = api_client.post(reverse('login', kwargs={'version': '1'}), data2)
    assert response_missing_email.status_code == 400
    assert response_missing_password.status_code == 400
