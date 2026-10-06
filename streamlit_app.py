import streamlit as st

from app import create_agent_executor


@st.cache_resource
def get_agent_executor():
    return create_agent_executor()


st.set_page_config(page_title="Agent Playground")
st.title("Agent Playground")
st.caption("Ask a question and let your research agent find an answer.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Ask your agent a question"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Researching..."):
            try:
                agent_executor = get_agent_executor()
                result = agent_executor.invoke({"input": question})
                answer = result["output"]
            except Exception as error:
                answer = f"Agent error: {error}"
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})