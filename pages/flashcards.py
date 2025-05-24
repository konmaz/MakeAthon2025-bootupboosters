import streamlit as st
import random

from gemini import FlashCard

st.set_page_config(page_title="Flashcards", layout="wide")
st.title("📚 Flashcards")

if "flashcard_data" not in st.session_state:
    st.warning("Please process content in the main page first to generate flashcards!")
else:
    # Initialize card state if not exists
    if "current_card" not in st.session_state:
        st.session_state.current_card = random.choice(st.session_state.flashcard_data)
        st.session_state.show_answer = False

    flashcards = st.session_state.flashcard_data
    
    if len(flashcards) > 0:
        # Center the content
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Create a card-like container
            with st.container(border=True):

                st.markdown(f"**{st.session_state.current_card.prompt}**")
                
                if st.button("Answer", use_container_width=True):
                    st.session_state.show_answer = not st.session_state.show_answer
                
                if st.session_state.show_answer:
                    st.markdown(f"{st.session_state.current_card.answer}")
            
            if st.button("Next Card", use_container_width=True):
                st.session_state.current_card = random.choice(flashcards)
                st.session_state.show_answer = False
                st.rerun()