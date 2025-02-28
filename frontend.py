import streamlit as st
import requests

st.title("Quiz Bot UI")

st.sidebar.header("Quiz Options")
category = st.sidebar.selectbox("Select Category", ["Science", "History", "Math"])

if st.sidebar.button("Create Quiz"):
    response = requests.post("http://127.0.0.1:5000/quiz/create", json={"category": category})
    st.success(response.json()["message"])

quiz_id = st.sidebar.number_input("Enter Quiz ID to Approve", min_value=1)
if st.sidebar.button("Approve Quiz"):
    response = requests.post(f"http://127.0.0.1:5000/quiz/approve/{quiz_id}")
    st.success(response.json()["message"])

if st.sidebar.button("Start Quiz"):
    response = requests.post(f"http://127.0.0.1:5000/quiz/start/{quiz_id}")
    if "quiz" in response.json():
        st.write(response.json()["quiz"])
    else:
        st.error(response.json()["error"])
