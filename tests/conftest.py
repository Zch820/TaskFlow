import pytest
from apps.tasks.models import Task
from model_bakery import baker
from apps.projects.models import Project
from apps.users.models import User
from rest_framework.test import APIClient

# ----- Users fixtures --------------------------------

# user 1
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='user', email="user@user.com",password="20")

@pytest.fixture
def auth_user(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


# user 2
@pytest.fixture
def user2():
    return User.objects.create_user(username='user2', email="user@two.com",password="20")

@pytest.fixture
def auth_user2(user2):
    api_client2 = APIClient()  # using a different api_client
    api_client2.force_authenticate(user=user2)
    return api_client2


# ----- Projects fixtures --------------------------------

@pytest.fixture
def user_projects(user):
    return baker.make(Project, _quantity=3, name='project', owner=user)

@pytest.fixture
def user2_projects(user2):
    return baker.make(Project, _quantity=2, name='project', owner=user2)


# ----- Tasks fixtures --------------------------------

@pytest.fixture
def user_tasks(user_projects):
    return baker.make(Task, _quantity=3, title='task', project=user_projects[0])


@pytest.fixture
def user2_tasks(user2_projects):
    return baker.make(Task, _quantity=2, title='task', project=user2_projects[0])


