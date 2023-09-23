import boto3
from botocore.exceptions import ClientError
import os
from boto3.dynamodb.types import TypeSerializer
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory
from langchain.memory import ConversationBufferMemory
from config import config

from datetime import datetime
import json

now = datetime.utcnow()
dynamodb = boto3.client('dynamodb')
ts = TypeSerializer()

openai_api_key_ssm_parameter_name = config.OPENAI_API_KEY_SSM_PARAMETER_NAME
chat_index_table_name = config.CONVERSATION_INDEX_TABLE_NAME
conversation_table_name = config.CONVERSATION_TABLE_NAME


class Chat():
    def __init__(self, event):
        print('init')
        self.set_user_number(event)
        self.set_chat_index()
        self.set_memory()
        print('init -- usernumber- '+self.user_number)
        print('init -- chat_index- ' + str(self.chat_index))
        print('init -- memory- '+str(self.memory))
        print('init -- message_history- '+str(self.message_history))
       
        print('init -- init end')

    def set_memory(self):
        print('set_memory')
        _id = self.user_number + "-" + str(self.chat_index)
        print('set_memory -- id- '+_id)
        print('set_memory -- conversation_table_name- '+conversation_table_name)
        self.message_history = DynamoDBChatMessageHistory(
            table_name=conversation_table_name, session_id=_id)
        print('set_memory --message_history from langchain/dynamodb - '+str(self.message_history))
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", chat_memory=self.message_history, return_messages=True)
        print('set_memory -- langchain memory- '+str(self.memory))

    
    def get_chat_index(self):
        print('get_chat_index')
        key = {'phone_number': self.user_number}
        serializedData = ts.serialize(key)
        
        try:
            print('getItem - chat_index_table_name - '+chat_index_table_name)
            print('getItem - serializedData - '+str(serializedData))
            print('getItem - key - '+str(key))
            
            chat_index = dynamodb.get_item(
                TableName=chat_index_table_name, Key=serializedData['M'])
            print('getItem - chat_index - '+str(chat_index))
            if 'Item' in chat_index:
                return int(chat_index['Item']['chat_index']['N'])
        except ClientError as e:
            print('getItem - ClientError - '+str(e))
            #print(e)
        return 0
        


    def increment_chat_index(self):
        print('increment_chat_index')
        self.chat_index += 1
        input = {
            'phone_number': self.user_number,
            'chat_index': self.chat_index,
            'updated_at': str(now)
        }
        try:
            print('increment_chat_index - InputData' + str(input))
            serialized_data = ts.serialize(input)
            print('increment_chat_index - serialized_data' + str(serialized_data))
            print('increment_chat_index - chat_index_table_name'+chat_index_table_name)
            
            dynamodb.put_item(TableName=chat_index_table_name,
                          Item=serialized_data['M'])
        except ClientError as e:
            print('increment_chat_index - ClientError - '+str(e))
            print(e)
        

    def create_new_chat(self):
        print('create_new_chat'+str(self))
        print('create_new_chat --> increment_chat_index')
        self.increment_chat_index()

    def set_user_number(self, event):
        print('set_user_number --> '+str(event)+' --> '+str(self))
        body = json.loads(event['body'])
        self.user_number = body['phoneNumber']
        print('set_user_number --> '+str(self.user_number))

    def set_chat_index(self):
        print('set_chat_index --> get_chat_index')
        self.chat_index = self.get_chat_index()

    def http_response(self, message):
        print('http_response - '+str(message)+' - '+str(self))
        return {
            'statusCode': 200,
            'body': json.dumps(message)
        }
