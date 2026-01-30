import pytest
from django.urls import reverse


# ------ Registration Tests ---------------------------------------------------

@pytest.mark.django_db
def test_registration_success(api_client):
    response = api_client.post(reverse('register'), {'email':'new@new.com', 'password':'TaskFlow_2026', 'confirm_password':'TaskFlow_2026'})
    assert response.status_code == 201

@pytest.mark.django_db
def test_registration_failure_password_match(api_client):
    response = api_client.post(reverse('register'),{'email': 'new@new.com', 'password':'TaskFlow_2026', 'confirm_password':'TaskFlow'})
    assert response.status_code == 400

@pytest.mark.django_db
def test_registration_failure_missing_fields(api_client):
    response_missing_email = api_client.post(reverse('register'),{'email': '', 'password':'TaskFlow_2026', 'confirm_password':'TaskFlow_2026'})
    response_missing_password = api_client.post(reverse('register'),{'email': 'new@new.com', 'password':''})
    assert response_missing_email.status_code == 400
    assert response_missing_password.status_code == 400

@pytest.mark.django_db
def test_registration_failure_existing_user(api_client, user):
    response = api_client.post(reverse('register'),{'email': 'user@user.com', 'password':'TaskFlow_2026', 'confirm_password':'TaskFlow_2026'})
    assert response.status_code == 400


# ------ Login Tests ---------------------------------------------------

@pytest.mark.django_db
def test_login_success(api_client, user):
    response = api_client.post(reverse('login'),{'email': 'user@user.com', 'password':'TaskFlow_2026'}, format="json")
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_failure_not_existing_user(api_client, user):
    response = api_client.post(reverse('login'), {'email': 'not@exist.com', 'password': 'TaskFlow_2026'})
    assert response.status_code == 401

@pytest.mark.django_db
def test_login_failure_wrong_password(api_client, user):
    response = api_client.post(reverse('login'), {'email': 'user@user.com', 'password': 'TaskFlow'})
    assert response.status_code == 401

@pytest.mark.django_db
def test_login_failure_missing_fields(api_client):
    response_missing_email = api_client.post(reverse('login'), {'email': '', 'password': 'TaskFlow_2026'})
    response_missing_password = api_client.post(reverse('login'), {'email': 'user@user.com', 'password': ''})
    assert response_missing_email.status_code == 400
    assert response_missing_password.status_code == 400
