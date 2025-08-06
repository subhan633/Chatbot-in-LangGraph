import streamlit as st
from chatbot_backend import workflow
from langchain_core.messages import HumanMessage

config = {'configurable': {'thread_id': '1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Load the conversational history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:

    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response = workflow.invoke({'messages': HumanMessage(content=user_input)}, config=config)
    ai_message = response['messages'][-1].content


    with st.chat_message('assistant'):
        
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in workflow.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config = {'configurable': {'thread_id': '1'}},
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})