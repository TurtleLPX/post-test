import streamlit as st

def init_session():
    st.session_state.setdefault("article_draft", "")
    st.session_state.setdefault("doc_url", "")
