import pytest
from django.urls import reverse
from django.utils import timezone

# ------ Tasks Create Tests ---------------------------------------------------

@pytest.mark.django_db
def test_create_task(auth_user, user_projects):
    project_id = user_projects[0].id
    data = {'title':'My Task', 'due_date':timezone.now().date()}
    response = auth_user.post(reverse('task-list', kwargs={'project_id':project_id}), data)
    assert response.status_code == 201

# ------ Tasks Read Tests -----------------------------------------------------

@pytest.mark.django_db
def test_listing_tasks(auth_user, auth_user2, user_projects, user2_projects, user_tasks, user2_tasks):
    # listing user tasks
    project_id = user_projects[0].id
    response_user = auth_user.get(reverse('task-list', kwargs={'project_id': project_id}))
    assert response_user.status_code == 200
    assert len(response_user.json()) == 3

    # listing user2 tasks
    project_id2 = user2_projects[0].id
    response_user2 = auth_user2.get(reverse('task-list', kwargs={'project_id': project_id2}))
    assert response_user2.status_code == 200
    assert len(response_user2.json()) == 2

@pytest.mark.django_db
def test_listing_tasks_failure_permission(auth_user, user2_projects, user2_tasks):
    project_id = user2_projects[0].id
    response = auth_user.get(reverse('task-list', kwargs={'project_id': project_id}))
    assert response.status_code == 403

@pytest.mark.django_db
def test_retrieving_task(auth_user, user_projects, user_tasks):
    project_id = user_projects[0].id
    task_id = user_tasks[0].id
    response = auth_user.get(reverse('task-detail', kwargs={'project_id': project_id, 'task_id': task_id}))
    assert response.status_code == 200

@pytest.mark.django_db
def test_retrieving_task_failure_permission(auth_user, user2_projects, user2_tasks):
    project_id = user2_projects[0].id
    task_id = user2_tasks[0].id
    response = auth_user.get(reverse('task-detail', kwargs={'project_id': project_id, 'task_id': task_id}))
    assert response.status_code == 403

# ------ Tasks Update Tests ---------------------------------------------------

@pytest.mark.django_db
def test_update_task(auth_user, user_projects, user_tasks):
    project_id = user_projects[0].id
    task_id = user_tasks[0].id
    data = {'title':'New Title', 'due_date':timezone.now().date()}
    response = auth_user.put(reverse('task-detail', kwargs={'project_id': project_id, 'task_id': task_id}),data)
    assert response.status_code == 200
    assert response.json()['title'] == 'New Title'

@pytest.mark.django_db
def test_update_task_failure_permission(auth_user, user2_projects, user2_tasks):
    project_id = user2_projects[0].id
    task_id = user2_tasks[0].id
    data = {'title':'New Title', 'due_date':timezone.now().date()}
    response = auth_user.put(reverse('task-detail', kwargs={'project_id': project_id, 'task_id': task_id}),data)
    assert response.status_code == 403

# ------ Tasks Delete Tests ---------------------------------------------------

@pytest.mark.django_db
def test_delete_task(auth_user, user_projects, user_tasks):
    project_id = user_projects[0].id
    task_id = user_tasks[0].id
    response = auth_user.delete(reverse('task-detail', kwargs={'project_id': project_id, 'task_id': task_id}))
    assert response.status_code == 204

@pytest.mark.django_db
def test_delete_task_failure_permission(auth_user, user2_projects, user2_tasks):
    project_id = user2_projects[0].id
    task_id = user2_tasks[0].id
    response = auth_user.delete(reverse('task-detail', kwargs={'project_id': project_id, 'task_id': task_id}))
    assert response.status_code == 403
