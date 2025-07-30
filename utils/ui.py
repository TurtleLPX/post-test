import streamlit as st

def inject_css():
    st.markdown(f"""
    <style>
        body {{
            background-color: #e9e6e2;
            color: #2f2f2f;
        }}
        .stFormSubmitButton > button,
        .stButton > button,
        div.row-widget.stButton {{
            background-color: #ab452b;
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 6px;
            font-weight: bold;
        }}
        .stButton > button:hover,
        .stFormSubmitButton > button:hover {{
            background-color: #93361f;
        }}
        .stTextInput > div > div > input,
        .stTextArea textarea {{
            background-color: #fefbf7;
            border: 1px solid #d4c7b9;
            font-family: 'Courier New', monospace;
        }}
        .stMarkdown h3 {{
            color: #ab452b;
            margin-top: 2rem;
        }}
    </style>
    """, unsafe_allow_html=True)
