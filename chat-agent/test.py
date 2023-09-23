from AIMessageProcessor import lambda_handler
import json

# Create an example event
# event = {
#     "inputTranscript": "what is escrow?",
#     "sessionId": "609-455-0028"
# }

#optionally the voice prompt will say "start a new conversation". This will trigger the agent to start a new conversation. 
event = {
    "inputTranscript": "what is loan modification?",
    "sessionId": "609-455-0028",
    "body": json.dumps({"phoneNumber": "609-455-0028", "message": "what is loan modification?"})
}




# Call the Lambda function
result = lambda_handler(event, None)

# Print the result
print(result)
