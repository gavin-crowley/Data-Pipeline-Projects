import requests
import json
import configparser
import csv
import boto3

# lat = 42.36
# lon = 71.05
# lat_log_params = {"lat": lat, "lon": lon}

api_response = requests.get(
    "http://api.open-notify.org/astros.json")
    # "http://api.open-notify.org/astros.json", params=lat_log_params)

# create a json object from the response content
response_json = json.loads(api_response.content)


all_people = []
for response in response_json['people']:
    current_person = []

    current_person.append(response['name'])
    current_person.append(response['craft'])

    all_people.append(current_person)

export_file = "rest_export_file.csv"

with open(export_file, 'w') as fp:
	csvw = csv.writer(fp, delimiter='|')
	csvw.writerows(all_people)

fp.close()

# # load the aws_boto_credentials values
parser = configparser.ConfigParser()
parser.read("pipeline.conf")
access_key = parser.get("aws_boto_credentials",
                "access_key")
secret_key = parser.get("aws_boto_credentials",
                "secret_key")
bucket_name = parser.get("aws_boto_credentials",
                "bucket_name")

s3 = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key)

s3.upload_file(
    export_file, 
    bucket_name,
    export_file)
