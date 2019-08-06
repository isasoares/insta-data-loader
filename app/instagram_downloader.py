import logging
import os

import instaloader

from . import file_utils
from .exceptions import NotEnoughPosts

logger = logging.getLogger(__name__)


class InstaDataProvider:

    def __init__(self, username):
        self.username = username
        self.loader = instaloader.Instaloader()
        self.profile = self.reload_profile()

    def reload_profile(self):
        """
        Load the profile data for the user

        :return: Profile object with the user's data
        """
        return instaloader.Profile.from_username(self.loader.context, self.username)

    def get_latest_posts(self, number_of_posts):
        """
        Get a number of posts from the profile data

        :param number_of_posts: how many posts it should look for at the profile data
        :return: list of the latest Post objects, with the size of number_of_posts
        """
        latest_posts = []
        posts = self.profile.get_posts()

        for i in range(number_of_posts):
            try:
                next_post = next(posts)
                latest_posts.append(next_post)
            except StopIteration:
                logger.warning(f'There are not enough posts. Only able to get {i} posts out of the {number_of_posts}.')
                raise NotEnoughPosts(number_of_posts, i)

        return latest_posts

    def save_compressed_posts(self, posts):
        """
        Save the profile data from instaloader to a compressed json file

        :param posts: list of Post objects that should be saved
        :return:
        """
        filenames = []
        file_utils.create_user_local_directory(self.username)

        for i, post in enumerate(posts):
            local_filename = os.path.join(file_utils.get_user_local_path(self.username),
                                          file_utils.get_post_filename(self.username, i))
            instaloader.save_structure_to_file(post, local_filename)
            filenames.append(local_filename)
            logger.info(f'Successfully saved file {local_filename}')

        return filenames

    def save_compressed_profile(self):
        """
        Save the profile data from instaloader to a compressed json file

        :return: filename used to save the file locally
        """
        file_utils.create_user_local_directory(self.username)
        local_filename = os.path.join(file_utils.get_user_local_path(self.username),
                                      file_utils.get_profile_filename(self.username))
        instaloader.save_structure_to_file(self.profile, local_filename)
        return local_filename

    def load_and_save_latest_posts(self, number_of_posts):
        """
        Save the posts data from instaloader to compressed json files

        :param number_of_posts: how many posts it should look for at the profile data
        :return: filenames used to save the files locally
        """
        latest_posts = self.get_latest_posts(number_of_posts)
        latest_posts_filenames = self.save_compressed_posts(latest_posts)
        return latest_posts_filenames
