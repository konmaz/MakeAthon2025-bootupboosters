import streamlit as st
import random

from gemini import FlashCard, Presentation

st.set_page_config(page_title="Presentation", layout="wide")
st.title("👩‍🏫 Presentation")

if "presentation" not in st.session_state:
    st.warning("Please process content in the main page first to generate presentation!")
else:
    st.session_state.presentation: list[Presentation]
    total_slides = len(st.session_state.presentation)

    # Initialize current slide index
    if "slide_index" not in st.session_state:
        st.session_state.slide_index = 0

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("Previous") and st.session_state.slide_index > 0:
            st.session_state.slide_index -= 1
    with col3:
        if st.button("Next") and st.session_state.slide_index < total_slides - 1:
            st.session_state.slide_index += 1

    # Ensure slide_index stays within valid range
    st.session_state.slide_index = max(0, min(st.session_state.slide_index, total_slides - 1))

    # Display current slide
    current_slide = st.session_state.presentation[st.session_state.slide_index]
    st.markdown(f"# {current_slide.headline}")
    st.markdown('\n'.join(f'- {item}' for item in current_slide.bullet_points))

    # Slide counter
    st.caption(f"Slide {st.session_state.slide_index + 1} of {total_slides}")
