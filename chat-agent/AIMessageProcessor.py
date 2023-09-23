import json
import os
import boto3
from langchain.chat_models import ChatOpenAI
from chat import Chat
from Agent import Agent
from config import config
from dotenv import load_dotenv

conversation_table_name = config.CONVERSATION_TABLE_NAME
openai_api_key_ssm_parameter_name = config.OPENAI_API_KEY_SSM_PARAMETER_NAME

def lambda_handler(event, context):
    print(event)
    if not is_http_request(event):
        event['body'] = {
            'message': event['inputTranscript'],
            'phoneNumber': event['sessionId']
        }
        event['body'] = json.dumps(event['body'])
    chat = Chat(event)
    set_openai_api_key()
    user_message = get_user_message(event)
    if is_user_request_to_start_new_conversation(event):
        chat.create_new_chat()
        return chat.http_response("Hi, I'm Gace,  Mortgage's digital assistant. What can I help you with today?")
    llm = ChatOpenAI(temperature=0, model_name="gpt-4")
    lex_agent = Agent(llm, chat.memory)
    message = lex_agent.run(input=user_message)
    if not is_http_request(event):
        return lex_response(event, message)
    return chat.http_response(message)

def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']
    return {}

def is_user_request_to_start_new_conversation(event):
    user_message = get_user_message(event)
    return "start a new conversation" in user_message.strip().lower()

def is_http_request(event):
    return 'headers' in event

def get_user_message(event):
    body = load_body(event)
    user_message_body = body['message']
    return user_message_body

def load_body(event):
    # if is_http_request(event):
    if True:
        body = json.loads(event['body'])
    else:
        body = json.loads(event['Records'][0]['Sns']['Message'])
    return body

def lex_response(event, message):
    # Return a response to Lex V2
    return {
        'sessionState': {
            'sessionAttributes': event['sessionState']['sessionAttributes'],
            'dialogAction': {
                'type': 'ElicitIntent'
            },
            'intent': {'name':event['sessionState']['intent']['name'], 'state': 'Fulfilled'}
        },
        'messages': [{
            'contentType': 'PlainText',
            'content': message
        }]
    }

def set_openai_api_key():
    #ssm = boto3.client('ssm')
    #response = ssm.get_parameter(Name=openai_api_key_ssm_parameter_name)
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY_SSM_PARAMETER_NAME") #response['Parameter']['Value']
