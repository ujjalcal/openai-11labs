from AIMessageProcessor import lambda_handler
import json

# Create an example event
# event = {
#     "inputTranscript": "what is escrow?",
#     "sessionId": "609-455-0028"
# }

event = {
    "inputTranscript": "Hi, I\'m Grace, Mortgage\'s digital assistant. What can I help you with today?",
    "sessionId": "609-455-0028",
    "body": json.dumps({"phoneNumber": "609-455-0028", "message": "what is loan modification?"})
}


# Call the Lambda function
result = lambda_handler(event, None)

# Print the result
print(result)
