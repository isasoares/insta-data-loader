import json


def test_upload_data_from_non_existing_user(client, non_existing_user):
    response = client.get(f'/{non_existing_user}/upload')
    message = json.loads(response.get_data().decode("utf-8").replace("'", '"')).get('message')
    assert f'Profile {non_existing_user} does not exist on Instagram' == message, \
        f'Did not received proper message when trying to upload data for non-existing user {non_existing_user}'
    assert response.status_code == 404, f'Status code is not 404'


def test_upload_data_from_user_with_less_than_ten_posts(client, user_with_few_posts):
    response = client.get(f'/{user_with_few_posts}/upload')
    message = json.loads(response.get_data().decode("utf-8").replace("'", '"')).get('message')
    assert 'There are not enough posts' in message, \
        f'Did not received proper message when trying to upload data for user with few posts {user_with_few_posts}'
    assert response.status_code == 412, f'Status code is not 412'


def test_upload_data_from_already_saved_user(client, saved_user, load_data_for_saved_user):
    response = client.get(f'/{saved_user}/upload')
    message = json.loads(response.get_data().decode("utf-8").replace("'", '"')).get('message')
    assert 'Files successfully uploaded to bucket' in message, \
        f'Did not received proper message when trying to upload data for already saved user {saved_user}'
    assert response.status_code == 201, f'Status code is not 201'


def test_upload_data_from_not_saved_user(client, not_saved_user, delete_data_for_not_saved_user):
    response = client.get(f'/{not_saved_user}/upload')
    message = json.loads(response.get_data().decode("utf-8").replace("'", '"')).get('message')
    assert 'Files successfully uploaded to bucket' in message, \
        f'Did not received proper message when trying to download profile for not saved user {not_saved_user}'
    assert response.status_code == 201, f'Status code is not 201'
