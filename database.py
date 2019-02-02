#!/usr/bin/python
import boto3
import MySQLdb
from botocore.exceptions import ClientError

# Get details of the all the IAM users and their SSH names from opsworks of the AWS account.

iam = boto3.client('iam')
client = boto3.client('opsworks')
paginator = iam.get_paginator('list_users')
for page in paginator.paginate():
        for user in page['Users']:
                try:
                        response = client.describe_user_profiles(
                                IamUserArns=[
                                        user['Arn']
                                ]
                        )
                        list = (response['UserProfiles'])
                        new_dict = {item['Name']:item for item in list}
                        dict =new_dict[user['UserName']]
                        IAM = dict['Name']

                        SSH = dict['SshUsername']

                except ClientError as e:
                        if e.response['Error']['Code'] == "ResourceNotFoundException":

                                pass

#The details of the database to which these data are to be uploaded. 

                host = "<HOST IP>"
                user = "<USER>"
                password = "<PASSWORD>"
                db = "<DATABASE_NAME>"
                conn = MySQLdb.connect(host, user, password, db)
                cursor = conn.cursor()
                sql = """INSERT INTO data(IAM_Username,SSH_Username) VALUES(%s, %s)"""
                args = (IAM, SSH)

                try:
                        # Execute the SQL command
                        cursor.execute(sql, args)
                        # Commit your changes in the database
                        conn.commit()
                except:
                        # Rollback in case there is any error
                        conn.rollback()
                # disconnect from server
                conn.close()
