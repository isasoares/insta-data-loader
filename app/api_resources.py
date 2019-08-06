import json
import logging
import lzma

from boto3.exceptions import S3UploadFailedError
from botocore.exceptions import ClientError
from flask_restful import Resource
from instaloader import ProfileNotExistsException

from . import config
from .instagram_downloader import InstaDataProvider
from .exceptions import NotEnoughPosts
from .s3_handler import S3Handler

logger = logging.getLogger(__name__)


class LoadProfileData(Resource):

    def get(self, username):
        bucket_name = config.BUCKET
        if not bucket_name:
            return {'message': f'Bucket name has not been provided'}, 412

        try:
            insta_data = InstaDataProvider(username)
        except ProfileNotExistsException:
            return {'message': f'Profile {username} does not exist on Instagram'}, 404

        profile = insta_data.save_compressed_profile()
        s3_handler = S3Handler(bucket_name)

        try:
            latest_posts = insta_data.load_and_save_latest_posts(10)
        except NotEnoughPosts as e:
            return {'message': e.message}, 412

        try:
            s3_handler.upload_profile_to_s3_bucket(profile)
            s3_handler.upload_posts_to_s3_bucket(latest_posts)
        except S3UploadFailedError:
            return {'message': f'Unable to upload files because bucket {bucket_name} does not exist.'}, 400

        return {'message': f'Files successfully uploaded to bucket {bucket_name}.'}, 201


class ProfilePost(Resource):

    def get(self, username, post):
        # post_json = None
        bucket_name = config.BUCKET
        if not bucket_name:
            return {'message': f'Bucket name has not been provided'}, 412

        s3_handler = S3Handler(bucket_name)
        try:
            local_filename = s3_handler.download_post_from_s3_bucket(username, post)
        except ClientError:
            return {'message': f'Unable to find post {post} from {username} on s3 bucket {bucket_name}'}, 404

        try:
            post_json = json.loads(lzma.open(local_filename).read())
        except:
            return {'message': f'Unable to load profile data'}, 500

        return post_json, 200


class ProfileData(Resource):

    def get(self, username):
        bucket_name = config.BUCKET
        if not bucket_name:
            return {'message': f'Bucket name has not been provided'}, 412

        s3_handler = S3Handler(bucket_name)
        try:
            local_filename = s3_handler.download_profile_from_s3_bucket(username)
        except ClientError:
            return {'message': f'Unable to find profile from user {username} on s3 bucket {bucket_name}'}, 404

        try:
            profile_json = json.loads(lzma.open(local_filename).read())
        except:
            return {'message': f'Unable to load profile data'}, 500

        return profile_json, 200
