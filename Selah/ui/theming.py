import streamlit as st

def set_theme():
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f2f6;
            color: #333333;
        }
        .sidebar .sidebar-content {
            background-color: #1e293b;
            color: white;
        }
        button, .stButton>button {
            background-color: #3b82f6;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def emoji_label(text, emoji):
    return f"{emoji} {text}"
