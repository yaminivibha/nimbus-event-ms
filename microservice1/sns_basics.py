"""test_aws_service_handler.py"""
import os
import boto3

def publish_message_to_sns(msg):
    sns_client = boto3.client(
            "sns", 
            region_name = 'us-east-1'
        )
        
    topic_arn = "arn:aws:sns:us-east-1:401581269557:EventUpdate"
    msg_id = sns_client.publish(
        TopicArn=topic_arn, 
        Message=msg
    )
    return msg_id

def testing():
    test_message = "test_message"
    message_id = publish_message_to_sns(test_message)

    if message_id["ResponseMetadata"]["HTTPStatusCode"] == 200:
        print("success!")
    else:
        print("fail")
    print(message_id)