import streamlit as st
import base64
import plotly.express as px
from ques import quiz_data  # Importing the quiz data from quiz_data.py

st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://i.pinimg.com/736x/db/34/d4/db34d40b271fb59477621550bf73ea0b.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }}
    
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        display: block;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.3);
        z-index: 0;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Rest of your Streamlit app code goes here

def show_question():
    question = quiz_data[st.session_state.selected_topic][st.session_state.current_question]
    st.write(f"Question {st.session_state.current_question + 1}: {question['question']}")
    
    # Disable radio button if question is already answered
    if st.session_state.current_question in st.session_state.answered_questions:
        selected_option = st.radio("Select your answer:", question['options'], key=f"option_{st.session_state.current_question}", disabled=True)
    else:
        selected_option = st.radio("Select your answer:", question['options'], key=f"option_{st.session_state.current_question}")

    col1, col2 = st.columns(2)
    with col2:
        if st.session_state.current_question < len(quiz_data[st.session_state.selected_topic]) - 1:
            if st.button("Next", key="next"):
                if st.session_state.current_question not in st.session_state.answered_questions:
                    check_answer(selected_option)
                next_question()
        else:
            if st.button("Complete Quiz", key="complete"):
                if st.session_state.current_question not in st.session_state.answered_questions:
                    check_answer(selected_option)
                st.session_state.quiz_completed = True
                st.session_state.page = "final_score"
                st.rerun()

    if not st.session_state.quiz_completed and st.session_state.current_question not in st.session_state.answered_questions:
        if st.button("Submit"):
            check_answer(selected_option)

# Function to check the selected answer
def check_answer(selected_option):
    question = quiz_data[st.session_state.selected_topic][st.session_state.current_question]
    if selected_option == question["correct_answer"]:
        st.write("Correct!")
        st.balloons()
        st.session_state.score += 1
    else:
        st.write("Incorrect!")
    st.write(f"Explanation: {question['correct_answer']}")
    st.session_state.answered_questions.add(st.session_state.current_question)  # Mark the question as answered

# Function to move to the next question
def next_question():
    if st.session_state.current_question < len(quiz_data[st.session_state.selected_topic]) - 1:
        st.session_state.current_question += 1
        st.rerun()  # Rerun to show the next question

# Function to display the final score and buttons
def show_final_page():
    st.markdown(f"<h1 style='text-align: center; color: white; font-size: 72px;'>Your Score: {st.session_state.score}/{len(quiz_data[st.session_state.selected_topic])}</h1>", unsafe_allow_html=True)

    # Buttons for "New Game" and "End"
    col1, col2 = st.columns(2)
    with col1:
        if st.button("New Game", key="new_game"):
            st.session_state.selected_topic = None
            st.session_state.quiz_completed = False
            st.session_state.score = 0
            st.session_state.current_question = 0
            st.session_state.answered_questions = set()
            st.session_state.page = "choose_topic"
            st.rerun()

    with col2:
        if st.button("End", key="end"):
            st.session_state.page = "end"
            st.rerun()

# Function to display the thank-you page
def show_end_page():
    st.markdown("<h1 style='text-align: center; color: white;'>Thank You for Using the Math Quiz!</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>We hope you enjoyed the quiz!</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Keep practicing, and see you next time!</h3>", unsafe_allow_html=True)
    st.image("https://www.example.com/thank_you_image.png", use_column_width=True)  # Add a creative image (replace the URL with your image URL)

# Main function
def main():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = None
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'page' not in st.session_state:
        st.session_state.page = "welcome"  # Default to welcome page
    if 'answered_questions' not in st.session_state:
        st.session_state.answered_questions = set()  # Set to track answered questions

    if st.session_state.page == "welcome":
        st.title("Welcome to Math Quiz")
        if st.button("Start"):
            st.session_state.page = "choose_topic"
            st.rerun()

    elif st.session_state.page == "choose_topic":
        st.title("Choose a Topic")
        topic = st.selectbox("Select a topic:", [
            "General Knowledge", "Science", "Mathematics", "Literature",
            "Entertainment", "Sports", "Geography", "History", "Arts and Culture"
        ])
        if st.button("Proceed"):
            st.session_state.selected_topic = topic
            st.session_state.current_question = 0
            st.session_state.page = "quiz"
            st.rerun()

    elif st.session_state.page == "quiz":
        if st.session_state.selected_topic and not st.session_state.quiz_completed:
            show_question()

    elif st.session_state.page == "final_score":
        show_final_page()

    elif st.session_state.page == "end":
        show_end_page()

if __name__ == "__main__":
    main()
