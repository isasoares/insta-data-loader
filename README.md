# Instagram data loader using s3

Project developed in Python to gather profile data and posts from user accounts on Instagram (using instaloader) and 
send them to a private AWS s3 bucket (using boto3).

# Environment setup

Clone this project from GitHub, then create a virtual environment using virtualenv with Python 3. 

`virtualenv -p python3 venv`

Then activate the newly created virtual environment, by running the following command:

`source venv/bin/activate`

After that, install the requirements by running the following command:

`pip3 install -r requirements.txt`

# Project execution

Fill in the config.py file with the s3 bucket name that will be used to download and upload data. 

To run the project, use the following command:

`python run.py`

# Features available

To load data from an Instagram user, then send their profile data and last 10 posts to a private s3 bucket, use the following endpoint, passing the desired username:

`/<string:username>/upload`

To get a specific post from an user, use the following endpoint, passing the desired username and the post index, which goes from 0 to 9, being 0 the most recent one:

`/<string:username>/<int:post>`

To get the profile information from an user, use the following endpoint, passing the desired username:

`/<string:username>`

# Tests

In order to run the tests, go to the main repo directory and run the following command:

`pytest`