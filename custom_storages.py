from storages.backends.s3boto3 import S3Boto3Storage

StaticRootS3BotoStorage = S3Boto3Storage(location='static')
MediaRootS3BotoStorage = S3Boto3Storage(location='media')
