import pytest
from django.urls import reverse


# ------ Project Create Tests ---------------------------------------------------

@pytest.mark.django_db
def test_create_project(auth_user):
    response = auth_user.post(reverse('v1_projects:project-list'), {'name': 'My Project'})
    assert response.status_code == 201


# ------ Project Read Tests ---------------------------------------------------

@pytest.mark.django_db
def test_listing_projects(auth_user, user_projects, user2_projects, auth_user2):
    # listing user projects
    response_user = auth_user.get(reverse('v1_projects:project-list'))
    assert response_user.status_code == 200
    assert len(response_user.json()) == 3

    # listing user2 projects
    response_user2 = auth_user2.get(reverse('v1_projects:project-list'))
    assert response_user2.status_code == 200
    assert len(response_user2.json()) == 2


@pytest.mark.django_db
def test_retrieve_project(auth_user, user_projects):
    response = auth_user.get(reverse('v1_projects:project-detail', kwargs={'pk': user_projects[0].id}))
    assert response.status_code == 200
    assert 'id' in response.json()
    assert 'name' in response.json()
    assert 'description' in response.json()


# ------ Project Update Tests ---------------------------------------------------

@pytest.mark.django_db
def test_update_project(auth_user, user_projects):
    response = auth_user.put(reverse('v1_projects:project-detail', kwargs={'pk': user_projects[0].id}),
                             {'name': 'New Name'})
    assert response.status_code == 200
    assert response.json()['name'] == 'New Name'


@pytest.mark.django_db
def test_update_project_failure_permission(auth_user, user_projects, auth_user2):
    response = auth_user2.put(reverse('v1_projects:project-detail', kwargs={'pk': user_projects[0].id}),
                              {'name': 'New Name'})
    assert response.status_code == 403


# ------ Project Delete Tests ---------------------------------------------------

@pytest.mark.django_db
def test_delete_project(auth_user, user_projects):
    response = auth_user.delete(reverse('v1_projects:project-detail', kwargs={'pk': user_projects[0].id}))
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_project_failure_permission(auth_user, user_projects, auth_user2):
    response = auth_user2.delete(reverse('v1_projects:project-detail', kwargs={'pk': user_projects[0].id}))
    assert response.status_code == 403
