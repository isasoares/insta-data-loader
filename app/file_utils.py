import logging
import os

from .config import ARTIFACTS_DIRECTORY

logger = logging.getLogger(__name__)


def create_local_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f'Directory created: {directory}')
    else:
        logger.info(f'Directory already exists: {directory}')


def get_profile_filename(username):
    return f'{username}_profile.json.xz'


def get_post_filename(username, post_index):
    return f'{username}_post_{post_index}.json.xz'


def get_user_local_path(username):
    return os.path.join(ARTIFACTS_DIRECTORY, username)


def create_user_local_directory(username):
    local_directory = get_user_local_path(username)
    create_local_directory(local_directory)
