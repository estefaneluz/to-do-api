import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import TaskItem, Tag
from .serializers import TaskItemSerializer, TagSerializer
from users.models import User

@pytest.mark.django_db
class TestTaskItemViews:
    def test_create_task(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'title': 'Nova tarefa'}
        response = client.post('/api/tasks/', data, format='json')
        assert response.status_code == 201
        assert 'id' in response.data
        assert 'title' in response.data

    def test_create_task_invalid_title(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'title': '', 'tags': []}
        response = client.post('/api/tasks/', data, format='json')
        assert response.status_code == 400
        assert 'title' in response.data

    def test_create_task_invalid_tags(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'title': 'Nova tarefa', 'tags': ['invalid_tag']}
        response = client.post('/api/tasks/', data, format='json')
        assert response.status_code == 400
        assert 'tags' in response.data

    # def test_update_task(self):
    #     user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
    #     token, _ = Token.objects.get_or_create(user=user)
    #     client = APIClient()
    #     client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    #     task = TaskItem.objects.create(title='Tarefa existente', created_by=user)
    #     data = {'title': 'Tarefa atualizada'}
    #     response = client.put(f'/api/tasks/{task.id}/', data, format='json')
    #     assert response.status_code == 200
    #     assert 'id' in response.data
    #     assert 'title' in response.data
    #     assert 'tags' in response.data
    
    # def test_update_task_empty_title(self):
    #     user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
    #     token, _ = Token.objects.get_or_create(user=user)
    #     client = APIClient()
    #     client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    #     task = TaskItem.objects.create(title='Tarefa existente', created_by=user)
    #     data = {'title': ''}
    #     response = client.put(f'/api/tasks/{task.id}/', data, format='json')
    #     assert response.status_code == 400
    #     assert 'title' in response.data

    def test_update_task(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        task = TaskItem.objects.create(title='Tarefa 1', created_by=user)
        data = {'title': 'Tarefa atualizada', 'status': 'DONE'}
        response = client.put(f'/api/tasks/{task.id}/update_task/', data, format='json')
        assert response.status_code == 200
        assert response.data['title'] == 'Tarefa atualizada'

    def test_update_task_invalid_status(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        task = TaskItem.objects.create(title='Tarefa 1', created_by=user)
        data = {'status': 'invalid'}
        response = client.put(f'/api/tasks/{task.id}/update_task/', data, format='json')
        assert response.status_code == 400
        assert 'status' in response.data

    def test_update_task_not_found(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'title': 'Tarefa atualizada'}
        response = client.put('/api/tasks/999/update_task/', data, format='json')
        assert response.status_code == 404

    def test_delete_task(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        task = TaskItem.objects.create(title='Tarefa existente', created_by=user)
        response = client.delete(f'/api/tasks/{task.id}/')
        assert response.status_code == 204

    def test_delete_task_not_exists(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.delete('/api/tasks/999/', format='json')
        assert response.status_code == 404

    def test_search_tasks(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        task1 = TaskItem.objects.create(title='Tarefa 1', created_by=user)
        task2 = TaskItem.objects.create(title='Tarefa 2', created_by=user)
        response = client.get('/api/tasks/', {'search': 'Tarefa'}, format='json')
        assert response.status_code == 200
        assert len(response.data.get('results')) == 2
        assert response.data.get('results')[0]['title'] == 'Tarefa 1'
        assert response.data.get('results')[1]['title'] == 'Tarefa 2'

    def test_search_tasks_empty(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('/api/tasks/', {'search': 'Não existe'}, format='json')
        assert response.status_code == 200
        assert len(response.data.get('results')) == 0

    def test_search_tasks_partial_match(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        task1 = TaskItem.objects.create(title='Tarefa 1', created_by=user)
        task2 = TaskItem.objects.create(title='Tarefa 2', created_by=user)
        response = client.get('/api/tasks/', {'search': 'Tare'}, format='json')
        assert response.status_code == 200
        assert len(response.data.get('results')) == 2
        assert response.data.get('results')[0]['title'] == 'Tarefa 1'
        assert response.data.get('results')[1]['title'] == 'Tarefa 2'

    def test_list_tasks_filter_tags(self):
      user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
      token, _ = Token.objects.get_or_create(user=user)
      client = APIClient()
      client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      task1 = TaskItem.objects.create(title='Tarefa 1', created_by=user)
      task2 = TaskItem.objects.create(title='Tarefa 2', created_by=user)
      tag1 = Tag.objects.create(name='Tag 1')
      tag2 = Tag.objects.create(name='Tag 2')
      task1.tags.add(tag1)
      task2.tags.add(tag2)
      response = client.get('/api/tasks/', {'tags': [tag1.id]}, format='json')
      assert response.status_code == 200
      assert len(response.data.get('results')) == 1

@pytest.mark.django_db
class TestTagViews:
    def test_create_tag(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'name': 'Nova tag'}
        response = client.post('/api/tags/', data, format='json')
        assert response.status_code == 201
        assert 'id' in response.data
        assert 'name' in response.data

    def test_create_tag_invalid_name(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'name': ''}
        response = client.post('/api/tags/', data, format='json')
        assert response.status_code == 400
        assert 'name' in response.data

    def test_update_tag(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        tag = Tag.objects.create(name='Tag existente')
        data = {'name': 'Tag atualizada'}
        response = client.put

    def test_list_tags(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        tag1 = Tag.objects.create(name='Tag 1')
        tag2 = Tag.objects.create(name='Tag 2')
        response = client.get('/api/tags/', format='json')
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]['name'] == 'Tag 1'
        assert response.data[1]['name'] == 'Tag 2'

    def test_list_tags_empty(self):
        user = User.objects.create_user(email='test@example.com', name='Test User', password='password')
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('/api/tags/', format='json')
        assert response.status_code == 200
        assert len(response.data) == 0