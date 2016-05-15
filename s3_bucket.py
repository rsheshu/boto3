#!/usr/bin/env python

import boto3, argparse, os
from subprocess import call

#session = boto3.Session('AKIAI6H266XCWYNBCDVQ', 'N8KhjfE3zMA3lf7jFBOUGrDRpK1P18RaU2jR276V')

arg_parser = argparse.ArgumentParser(description='Script to upload files file to S3 bucket')
arg_parser.add_argument('-l', '--list', help='List the contents of the bucket', action="store_true")
arg_parser.add_argument('-u', '--file', help='Specify a file to upload. Must specify destination as well: \'-d/--destination\'')
arg_parser.add_argument('-D', '--destination', help='Specify the destination directory to upload files to')
arg_parser.add_argument('-d', '--directory', help='Upload the contents of a directory. Must specify destination as well: \'-d/--destination\'')
args = arg_parser.parse_args()

s3 = boto3.resource('s3')
bucket = s3.Bucket('gibb-bucket')

def list_bucket():
    for obj in bucket.objects.all():
        print obj.key

def upload_file():
    files = args.file
    file_basename = os.path.basename(files)
    destination = os.path.normpath(args.destination)
    s3.meta.client.upload_file(files, 'gibb-bucket', os.path.join(destination, file_basename))

def upload_directory():
    directory = os.path.normpath(args.directory)
    destination = os.path.normpath(args.destination)
    call(['aws', 's3', 'cp', '--recursive', directory, 's3://gibb-bucket/' + str(destination)])


if __name__ == '__main__':
    if args.list:
        list_bucket()
    if args.file:
        upload_file()
    if args.directory:
        upload_directory()
