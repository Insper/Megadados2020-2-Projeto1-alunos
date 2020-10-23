# pylint: disable=missing-module-docstring,missing-function-docstring
import os.path

from fastapi.testclient import TestClient

from utils import utils

from tasklist.main import app

client = TestClient(app)

app.dependency_overrides[utils.get_config_filename] = \
    utils.get_config_test_filename


def setup_database():
    scripts_dir = os.path.join(
        os.path.dirname(__file__),
        '..',
        'database',
        'migrations',
    )
    config_file_name = utils.get_config_test_filename()
    secrets_file_name = utils.get_admin_secrets_filename()
    utils.run_all_scripts(scripts_dir, config_file_name, secrets_file_name)


def test_read_main_returns_not_found():
    setup_database()
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_read_tasks_with_no_task():
    setup_database()
    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == {}


def test_create_and_read_some_tasks():
    setup_database()
    tasks = [
        {
            "description": "foo",
            "completed": False
        },
        {
            "description": "bar",
            "completed": True
        },
        {
            "description": "baz"
        },
        {
            "completed": True
        },
        {},
    ]
    expected_responses = [
        {
            'description': 'foo',
            'completed': False
        },
        {
            'description': 'bar',
            'completed': True
        },
        {
            'description': 'baz',
            'completed': False
        },
        {
            'description': 'no description',
            'completed': True
        },
        {
            'description': 'no description',
            'completed': False
        },
    ]

    # Insert some tasks and check that all succeeded.
    uuids = []
    for task in tasks:
        response = client.post("/task", json=task)
        assert response.status_code == 200
        uuids.append(response.json())

    # Read the complete list of tasks.
    def get_expected_responses_with_uuid(completed=None):
        return {
            uuid_: response
            for uuid_, response in zip(uuids, expected_responses)
            if completed is None or response['completed'] == completed
        }

    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == get_expected_responses_with_uuid()

    # Read only completed tasks.
    for completed in [False, True]:
        response = client.get(f'/task?completed={str(completed)}')
        assert response.status_code == 200
        assert response.json() == get_expected_responses_with_uuid(completed)

    # Delete all tasks.
    for uuid_ in uuids:
        response = client.delete(f'/task/{uuid_}')
        assert response.status_code == 200

    # Check whether there are no more tasks.
    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == {}


def test_substitute_task():
    setup_database()

    # Create a task.
    task = {'description': 'foo', 'completed': False}
    response = client.post('/task', json=task)
    assert response.status_code == 200
    uuid_ = response.json()

    # Replace the task.
    new_task = {'description': 'bar', 'completed': True}
    response = client.put(f'/task/{uuid_}', json=new_task)
    assert response.status_code == 200

    # Check whether the task was replaced.
    response = client.get(f'/task/{uuid_}')
    assert response.status_code == 200
    assert response.json() == new_task

    # Delete the task.
    response = client.delete(f'/task/{uuid_}')
    assert response.status_code == 200


def test_alter_task():
    setup_database()

    # Create a task.
    task = {'description': 'foo', 'completed': False}
    response = client.post('/task', json=task)
    assert response.status_code == 200
    uuid_ = response.json()

    # Replace the task.
    new_task_partial = {'completed': True}
    response = client.patch(f'/task/{uuid_}', json=new_task_partial)
    assert response.status_code == 200

    # Check whether the task was altered.
    response = client.get(f'/task/{uuid_}')
    assert response.status_code == 200
    assert response.json() == {**task, **new_task_partial}

    # Delete the task.
    response = client.delete(f'/task/{uuid_}')
    assert response.status_code == 200


def test_read_invalid_task():
    setup_database()

    response = client.get('/task/invalid_uuid')
    assert response.status_code == 422


def test_read_nonexistant_task():
    setup_database()

    response = client.get('/task/3668e9c9-df18-4ce2-9bb2-82f907cf110c')
    assert response.status_code == 404


def test_delete_invalid_task():
    setup_database()

    response = client.delete('/task/invalid_uuid')
    assert response.status_code == 422


def test_delete_nonexistant_task():
    setup_database()

    response = client.delete('/task/3668e9c9-df18-4ce2-9bb2-82f907cf110c')
    assert response.status_code == 404


def test_delete_all_tasks():
    setup_database()

    # Create a task.
    task = {'description': 'foo', 'completed': False}
    response = client.post('/task', json=task)
    assert response.status_code == 200
    uuid_ = response.json()

    # Check whether the task was inserted.
    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == {uuid_: task}

    # Delete all tasks.
    response = client.delete('/task')
    assert response.status_code == 200

    # Check whether all tasks have been removed.
    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == {}
