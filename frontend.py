import streamlit as st
import requests

# Initialize the session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("Travel Agent Chatbot")

# Input box for user query
query = st.text_input("Ask your travel-related question:")

if st.button("Submit"):
    if query:
        try:
            # Send the query to the FastAPI server
            response = requests.post("http://127.0.0.1:8000/query/", json={"query": query})
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            # Save the query and response to the session state
            st.session_state.chat_history.append({"query": query, "response": data["response"]})
        except requests.exceptions.RequestException as e:
            st.write("HTTP error occurred:", e)
        except Exception as e:
            st.write("An error occurred:", e)
    else:
        st.write("Please enter a query.")

# Display the chat history
st.write("Chat History:")
for chat in st.session_state.chat_history:
    st.write(f"**You:** {chat['query']}")
    st.write(f"**Bot:** {chat['response']}")
