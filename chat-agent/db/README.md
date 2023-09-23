
# for Conversation History Table
aws dynamodb create-table --cli-input-json file://conversation_history_table.json

# for chat inde table
aws dynamodb create-table --cli-input-json file://./chat_index_table.json

