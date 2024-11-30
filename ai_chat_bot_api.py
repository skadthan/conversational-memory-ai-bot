from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
import logging

import create_llm_instance
import get_IAM_usrID

logging.basicConfig(level=logging.CRITICAL)

# Initialize the DynamoDB chat message history
session_table_name = "SessionTable"
user_session_id = get_IAM_usrID.get_iam_user_id()  # You can make this dynamic based on the user session
history = DynamoDBChatMessageHistory(table_name=session_table_name, session_id=user_session_id)

# Create the chat prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

# Create output parser to simplify the output
output_parser = StrOutputParser()

# Combine the prompt with the Bedrock LLM
model=create_llm_instance.claude_llm();
chain = prompt | model| output_parser

# Integrate with message history
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda user_session_id: DynamoDBChatMessageHistory(
        table_name=session_table_name, session_id=user_session_id
    ),
    input_messages_key="question",
    history_messages_key="history",
)

# Invoke the chain with a session-specific configuration

#config = {"configurable": {"session_id": user_session_id}}

#response = chain_with_history.invoke({"question": "Hi! What is your name?"}, config=config)
#print(response)

#response = chain_with_history.invoke({"question": "And, my name is Suresh"}, config=config)
#print(response)

#response = chain_with_history.invoke({"question": "What's my name?"}, config=config)
#print(response)

