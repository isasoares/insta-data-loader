import json


def test_download_profile_from_not_saved_user(client, not_saved_user, delete_data_for_not_saved_user):
    response = client.get(f'/{not_saved_user}')
    message = json.loads(response.get_data().decode("utf-8").replace("'", '"')).get('message')
    assert f'Unable to find profile from user {not_saved_user}' in message, \
        f'Did not received proper message when trying to download profile for non-saved user {not_saved_user}'
    assert response.status_code == 404, f'Status code is not 404'


def test_download_profile_from_saved_user(client, saved_user, load_data_for_saved_user):
    response = client.get(f'/{saved_user}')
    assert response.is_json, f'Could not load profile from saved user {saved_user}'
    assert response.status_code == 200, f'Status code is not 200'


def test_download_saved_post_from_saved_user(client, saved_user, saved_post, load_data_for_saved_user):
    response = client.get(f'/{saved_user}/{saved_post}')
    assert response.is_json, f'Could not load post from saved user {saved_user}'
    assert response.status_code == 200, f'Status code is not 200'


def test_download_not_saved_post_from_saved_user(client, saved_user, not_saved_post, load_data_for_saved_user):
    response = client.get(f'/{saved_user}/{not_saved_post}')
    message = json.loads(response.get_data().decode("utf-8").replace("'", '"')).get('message')
    assert f'Unable to find post {not_saved_post} from {saved_user}' in message, \
        f'Did not received proper message when trying to download profile for saved user {saved_user}'
    assert response.status_code == 404, f'Status code is not 404'
