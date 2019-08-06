import logging
import os

import boto3

from . import file_utils

logger = logging.getLogger(__name__)


class S3Handler:

    def __init__(self, bucket):
        self.bucket = bucket
        self.s3 = boto3.client('s3')

    def upload_file_to_s3_bucket(self, bucket_filename, local_filename):
        """
        Upload to the s3 bucket a file that is stored locally

        :param bucket_filename: filename that will be used to store the file in the s3 bucket
        :param local_filename: filename used to store the file locally
        :return:
        """
        self.s3.upload_file(local_filename, self.bucket, bucket_filename)

    def download_file_from_s3_bucket(self, bucket_filename, local_filename):
        """
        Download from the s3 bucket a file that will be stored locally

        :param bucket_filename: filename used to store the file in the s3 bucket
        :param local_filename: filename that will be used to store the file locally
        :return:
        """
        self.s3.download_file(self.bucket, bucket_filename, local_filename)

    def upload_profile_to_s3_bucket(self, local_profile):
        """
        Upload to the s3 bucket a Profile compressed file that is stored locally

        :param local_profile: name of the file which contains the Profile data
        :return:
        """
        bucket_filename = os.path.basename(local_profile)
        self.upload_file_to_s3_bucket(bucket_filename, local_profile)

    def upload_posts_to_s3_bucket(self, local_posts):
        """
        Upload to the s3 bucket Post compressed files that are stored locally

        :param local_posts: list with the names of the files which contain the Posts data
        :return:
        """
        for local_post in local_posts:
            bucket_filename = os.path.basename(local_post)
            self.upload_file_to_s3_bucket(bucket_filename, local_post)

    def download_profile_from_s3_bucket(self, username):
        """
        Download from the s3 bucket a Profile compressed file that will be stored locally

        :param username: name of the user whose data will be downloaded
        :return: filename used to store the file locally
        """
        file_utils.create_user_local_directory(username)
        local_filename = os.path.join(file_utils.get_user_local_path(username),
                                      file_utils.get_profile_filename(username))
        bucket_filename = os.path.basename(local_filename)
        self.download_file_from_s3_bucket(bucket_filename, local_filename)
        return local_filename

    def download_post_from_s3_bucket(self, username, post_index):
        """
        Download from the s3 bucket a Post compressed file that will be stored locally

        :param username: name of the user whose data will be downloaded
        :param post_index: index of the post that will be downloaded, being 0 the most recent one and so on
        :return: filename used to store the file locally
        """
        file_utils.create_user_local_directory(username)
        bucket_filename = file_utils.get_post_filename(username, post_index)
        local_filename = os.path.join(file_utils.get_user_local_path(username), bucket_filename)
        self.download_file_from_s3_bucket(bucket_filename, local_filename)
        return local_filename

    def delete_user_files_from_s3_bucket(self, username):
        """
        Delete profile and post files of a user from the s3 bucket

        :param username: name of the user whose data will be deleted
        """
        post_filenames = [file_utils.get_post_filename(username, i) for i in range(10)]
        profile_filename = file_utils.get_profile_filename(username)
        files_to_delete = post_filenames + [profile_filename]
        for filename in files_to_delete:
            self.s3.delete_object(Bucket=self.bucket, Key=filename)
