import pytest

from ..app import create_app
from ..app.config import BUCKET
from ..app.instagram_downloader import InstaDataProvider
from ..app.s3_handler import S3Handler


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def s3_handler():
    return S3Handler(BUCKET)


@pytest.fixture
def insta_data_provider(saved_user):
    return InstaDataProvider(saved_user)


@pytest.fixture
def delete_data_for_not_saved_user(s3_handler, not_saved_user):
    s3_handler.delete_user_files_from_s3_bucket(not_saved_user)


@pytest.fixture
def load_data_for_saved_user(insta_data_provider, s3_handler):
    profile = insta_data_provider.save_compressed_profile()
    latest_posts = insta_data_provider.load_and_save_latest_posts(10)
    s3_handler.upload_profile_to_s3_bucket(profile)
    s3_handler.upload_posts_to_s3_bucket(latest_posts)


@pytest.fixture
def saved_user():
    return 'pythonbrasil'


@pytest.fixture
def not_saved_user():
    return 'pythonnordeste'


@pytest.fixture
def non_existing_user():
    return 'pythonbrasilaaaaaaaaaaa'


@pytest.fixture
def user_with_few_posts():
    return 'python'


@pytest.fixture
def saved_post():
    return 1


@pytest.fixture
def not_saved_post():
    return 100
