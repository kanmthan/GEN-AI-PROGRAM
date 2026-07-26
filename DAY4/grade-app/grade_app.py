import streamlit as st

st.set_page_config(
    page_title="Student Grade Calculator",
    page_icon="🎓",
    layout="centered"
)


def calculate_grade(mark):
    if 90 <= mark <= 100:
        return "A"
    elif 80 <= mark <= 89:
        return "B"
    elif 70 <= mark <= 79:
        return "C"
    elif 60 <= mark <= 69:
        return "D"
    else:
        return "E"


st.title("🎓 Student Grade Calculator")

st.write("Enter a mark between **0 and 100** to calculate the grade.")

mark = st.slider(
    "Select your mark",
    min_value=0,
    max_value=100,
    value=50
)

if st.button("Calculate Grade"):
    grade = calculate_grade(mark)

    st.success(f"Mark: **{mark}**")
    st.info(f"Grade: **{grade}**")

    if grade == "A":
        st.balloons()