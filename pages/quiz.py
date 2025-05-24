import streamlit as st
import random



st.set_page_config(page_title="4-Button Quiz", layout="wide")
st.title("🧠 4-Button Quiz")

# Check for quiz data
if "quiz_data" not in st.session_state:
    st.warning("Please process content in the main page first to generate quiz questions!")
else:
    # Initialize state
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.shuffled_answers = []

    quiz = st.session_state.quiz_data
    total = len(quiz)
    index = st.session_state.current_question

    if index >= total:
        st.success(f"🎉 Quiz complete! Final Score: {st.session_state.score}/{total}")

        a, b = st.columns(2)

        st.metric("Correct questions", st.session_state.score, st.session_state.score - total)
        st.metric("Total questions", total, )

        if st.button("Reset Quiz"):
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.shuffled_answers = []
            st.rerun()
    else:
        q = quiz[index]  # This is a QuizQuestion object
        st.progress((st.session_state.current_question + 1) / len(quiz))
        st.subheader(f"Question {index + 1} of {total}")
        st.markdown(f"**{q.question}**")

        if not st.session_state.shuffled_answers:
            answers = [q.correct_answer] + q.incorrect_answers
            random.shuffle(answers)
            st.session_state.shuffled_answers = answers

        # st.markdown("""
        #     <style>
        #     [data-testid="stMarkdownContainer"] {
        #         font-size: 2px;
        #     }
        #     </style>
        # """, unsafe_allow_html=True)
        message = None
        cols = st.columns(2)
        for i, answer in enumerate(st.session_state.shuffled_answers):
            with cols[i % 2]:
                if st.button(answer, disabled=st.session_state.answered, use_container_width=True):
                    st.session_state.answered = True
                    if answer == q.correct_answer:
                        message = True
                        st.session_state.score += 1
                        st.balloons()
                    else:
                        message = False

        if message is not None:
            if message:
                st.success("✅ Correct!")
            elif not message:
                st.error(f"❌ Wrong! Correct answer: **{q.correct_answer}**")

        if st.session_state.answered:
            if st.button("Next"):
                st.session_state.current_question += 1
                st.session_state.answered = False
                st.session_state.shuffled_answers = []
                st.rerun()