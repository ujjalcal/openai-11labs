
# for Conversation History Table
aws dynamodb create-table --cli-input-json file://conv-hist-table.jso

# for chat inde table
aws dynamodb create-table --cli-input-json file://chat_index_table.json

