from botocore.exceptions import ClientError

import logging
import os
import boto3
import json

def create_presigned_url(object_name):
    s3_client = boto3.client('s3',
                             region_name=os.environ.get('S3_PERSISTENCE_REGION'),
                             config=boto3.session.Config(signature_version='s3v4',s3={'addressing_style': 'path'}))
    try:
        bucket_name = os.environ.get('S3_PERSISTENCE_BUCKET')
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=60*60)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

def load_json_from_path(file_path):
    with open(file_path) as f:
        return json.load(f)

def create_single_video_playlist(playlist,video_number):
    return { "videoplayerData": {
                "type": "object",
                "properties": {
                    "playlist": [playlist[video_number]]
                    }
            }
        }

def create_all_video_playlist(playlist):
    return { "videoplayerData": {
                "type": "object",
                "properties": {
                    "playlist": playlist
                    }
            }
        }