#!/usr/bin/env python

import boto3, argparse
from subprocess import call
from os import path

arg_parser = argparse.ArgumentParser(description='Script to upload files file to S3 bucket')
arg_parser.add_argument('--list', help='List the contents of the bucket', action="store_true")
arg_parser.add_argument('--upload', help='Specify a file to upload to S3. Must specify destination as well: \'-d/--destination\'')
arg_parser.add_argument('--download', help='Specify a file to download from S3. Must specify destination as well: \'-d/--destination\'')
arg_parser.add_argument('--upload-dir', help='Upload the contents of a directory to S3. Must specify destination as well: \'-d/--destination\'')
arg_parser.add_argument('--download-dir', help='Downloads the contents of a directory from S3. Must specify destination as well: \'-d/--destination\'')
arg_parser.add_argument('--destination', help='Specify the destination directory to upload files to')
args = arg_parser.parse_args()

s3 = boto3.resource('s3')
bucket = s3.Bucket('gibb-bucket')
path = os.path()

'''
Add section to check for .config and .creds section?
'''

def if_location_exists(location):
    try:
        path.exists(location)
    except IOError:
        print "File or directory does not exist"
'''
Need to add destination dir to list
'''
def list_bucket():
    for obj in bucket.objects.all():
        print obj.key

def upload_file():
    files = args.upload
    file_basename = path.basename(files)
    destination = path.normpath(args.destination)
    if_location_exists(files)
    s3.meta.client.upload_file(files, str(bucket), path.join(destination, file_basename))

def download_file():
    files = args.download
    file_basename = path.basename(files)
    destination = path.normpath(args.destination)
    s3.meta.client.download_file(files, str(bucket), path.join(destination, file_basename))

def upload_directory():
    directory = path.normpath(args.upload-dir)
    destination = path.normpath(args.destination)
    if_location_exists(directory)
    call(['aws', 's3', 'cp', '--recursive', directory, 's3://' + str(bucket) + '/' + str(destination)])

def download_directory():
    directory = path.normpath(args.download_dir)
    destination = path.normpath(args.destination)
    if_location_exists(destination)
    call(['aws', 's3', 'cp', '--recursive', 's3://' + str(bucket) + '/' + str(directory), str(destination)])

'''
Cleaner way of doing this?
'''
if __name__ == '__main__':
    if args.list:
        list_bucket()
    if args.upload:
        upload_file()
    if args.upload-dir:
        upload_directory()
    if args.upload:
        download_file()
    if args.upload-dir:
        download_directory()
