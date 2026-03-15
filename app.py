import streamlit as st
import requests 

st.title("llama for Mobile")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are an ai assistant. Provide direct answers without unnecessary fluff"}]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("what is on your mind?")

if prompt:
     with st.chat_message("user"):
        st.markdown(prompt)

     st.session_state.messages.append({"role" : "user" , "content": prompt})
   

url = "http://localhost:11434/api/chat"

payload = {
    "model" : "llama3.2:1b",
    "messages" : st.session_state.messages,
    "stream" : True
}
response  = requests.post(url , json=payload)

full_response = ""
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    
   
    for line in response.iter_lines():
        if line:
            
            import json
            chunk = json.loads(line.decode("utf-8"))
            
            if "message" in chunk:
                token = chunk["message"]["content"]
                full_response += token
            
           
            message_placeholder.markdown(full_response + "▌")

    
    message_placeholder.markdown(full_response)


st.session_state.messages.append({"role": "assistant", "content": full_response})
