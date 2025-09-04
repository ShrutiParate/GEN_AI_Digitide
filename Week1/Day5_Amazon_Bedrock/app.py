import streamlit as st
import boto3
import json


# Streamlit UI

st.set_page_config(page_title="Bedrock Chat", page_icon="🤖")
st.title("🤖 Chat with Claude 3 Haiku (AWS Bedrock)")


# AWS Bedrock Client

client = boto3.client(
    service_name="bedrock-runtime",
    region_name=st.secrets["AWS_DEFAULT_REGION"],
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
)


# Chat Input

user_query = st.chat_input("Ask me anything...")

if user_query:
    with st.spinner("Thinking..."):
        # Prepare request payload
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 256,
            "temperature": 0.7,
            "messages": [
                {"role": "user", "content": user_query}
            ],
        }

        response = client.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            body=json.dumps(body)
        )

        # Parse response
        result = json.loads(response["body"].read())
        answer = result["content"][0]["text"]

        # Display chat
        st.chat_message("user").write(user_query)
        st.chat_message("assistant").write(answer)
