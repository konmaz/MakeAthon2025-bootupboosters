import streamlit as st
from streamlit_markmap import markmap

st.set_page_config(page_title="mind map", layout="wide")
st.title("Mind 🧠 map 🗺️")
if "mindmap" not in st.session_state:
    st.warning("Please process content in the main page first to generate mind maps!")
else:
    # Initialize card state if not exists
    print("here it is")
    print(st.session_state.mindmap)
    markmap(st.session_state.mindmap, height=700)


