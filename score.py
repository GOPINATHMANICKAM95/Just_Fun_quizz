import streamlit as st
import random

# Sample question data
questions = [
    {"question": "Who was the first Governor-General of independent India?", 
     "options": ["Lord Mountbatten", "C. Rajagopalachari", "Dr. Rajendra Prasad", "Mahatma Gandhi"], 
     "answer": "Lord Mountbatten"},
    {"question": "When was the Quit India Movement launched?", 
     "options": ["1942", "1932", "1922", "1952"], 
     "answer": "1942"},
    {"question": "Who gave the slogan 'Do or Die'?", 
     "options": ["Mahatma Gandhi", "Subhash Chandra Bose", "Jawaharlal Nehru", "Sardar Patel"], 
     "answer": "Mahatma Gandhi"},
    {"question": "In which year was the Non-Cooperation Movement called off by Gandhiji?", 
     "options": ["1922", "1920", "1919", "1930"], 
     "answer": "1922"},
    {"question": "Who was known as the 'Iron Man of India'?", 
     "options": ["Sardar Vallabhbhai Patel", "Bhagat Singh", "Bal Gangadhar Tilak", "Jawaharlal Nehru"], 
     "answer": "Sardar Vallabhbhai Patel"}
]

# Initialize scoreboard (persistent across different sessions)
if "scoreboard" not in st.session_state:
    st.session_state["scoreboard"] = {}

# Function to ask questions
def ask_questions(shuffled_questions):
    user_answers = []
    
    for i, q in enumerate(shuffled_questions):
        st.write(f"Q{i + 1}: {q['question']}")
        
        # Use checkboxes for answer selection
        options = q["options"]
        selected_option = None
        
        # Display checkboxes
        for option in options:
            if st.checkbox(option, key=f"q{i}_{option}"):
                selected_option = option
        
        user_answers.append(selected_option)
    
    return user_answers

# Function to reset checkboxes
def reset_checkboxes(shuffled_questions):
    for i, q in enumerate(shuffled_questions):
        for option in q["options"]:
            # Reset the checkbox state
            st.session_state[f"q{i}_{option}"] = False

# Display header
st.title("🇮🇳 Indian Freedom Struggle Quiz")

# Step 1: Collect username
username = st.text_input("Enter your username", max_chars=20, placeholder="Type your name...")

# Step 2: Initialize quiz for the user
if username:
    if "current_user" not in st.session_state or st.session_state["current_user"] != username:
        # New user starts the quiz; shuffle questions
        st.session_state["current_user"] = username
        st.session_state["shuffled_questions"] = random.sample(questions, len(questions))

    # Welcome the user
    st.write(f"Hello, {username}! Let's start the quiz. 🎉")

    # Step 3: Display questions and get the answers
    user_answers = ask_questions(st.session_state["shuffled_questions"])

    if st.button("Submit Quiz"):
        # Calculate score
        score = sum(1 for i, q in enumerate(st.session_state["shuffled_questions"]) if user_answers[i] == q['answer'])
        
        # Step 4: Add score to the scoreboard if the user hasn't already taken the quiz
        if username not in st.session_state["scoreboard"]:
            st.session_state["scoreboard"][username] = score

        # Sort the scoreboard by scores in descending order
        sorted_scoreboard = sorted(st.session_state["scoreboard"].items(), key=lambda x: x[1], reverse=True)
        
        # Find the user's rank
        user_rank = sorted_scoreboard.index((username, score)) + 1
        
        # Step 5: Display the user's score and rank
        st.success(f"🎉 Congratulations, {username}! Your score is **{score}/{len(questions)}**.")
        st.info(f"🏆 Your rank is **#{user_rank}** out of {len(sorted_scoreboard)} participants.")
        
        # Step 6: Display detailed scoreboard with all users
        st.subheader("📊 Scoreboard:")
        for i, (user, user_score) in enumerate(sorted_scoreboard):
            st.write(f"🏅 **{i + 1}. {user}** - Score: **{user_score}/{len(questions)}**")

        # Show the correct/incorrect answers for this user
        st.subheader(f"{username}'s Results:")
        for i, q in enumerate(st.session_state["shuffled_questions"]):
            if user_answers[i] == q['answer']:
                st.write(f"Q{i + 1}: ✅ Correct! The answer was **{q['answer']}**.")
            else:
                st.write(f"Q{i + 1}: ❌ Incorrect. The correct answer was **{q['answer']}**.")
        
        # Reset checkboxes for the next attempt
        reset_checkboxes(st.session_state["shuffled_questions"])
