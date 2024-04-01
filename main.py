import streamlit as st
import json
import datetime
import pandas as pd

def load_exercise_log():
    try:
        with open('exercise_log.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_exercise_log(exercise_log):
    with open('exercise_log.json', 'w') as file:
        json.dump(exercise_log, file, indent=4)

def track_exercise(date, pushups, squats, crunches):
    exercise_log = load_exercise_log()
    str_date = str(date)
    if str_date in exercise_log:
        # If the date already exists, add the counts to the existing data
        exercise_log[str_date]['pushups'] += pushups
        exercise_log[str_date]['squats'] += squats
        exercise_log[str_date]['crunches'] += crunches
    else:
        # If it's a new date, create a new entry
        exercise_log[str_date] = {
            'pushups': pushups,
            'squats': squats,
            'crunches': crunches
        }
    save_exercise_log(exercise_log)

def main():
    st.title('Exercise Tracker')

    today = datetime.date.today()

    pushups = st.number_input("Enter the number of pushups you did today:", min_value=0)
    squats = st.number_input("Enter the number of squats you did today:", min_value=0)
    crunches = st.number_input("Enter the number of crunches you did today:", min_value=0)

    if st.button("Log Exercises"):
        track_exercise(today, pushups, squats, crunches)
        st.success("Exercise count logged successfully.")

    if st.button("Show Exercise Progress"):
        exercise_log = load_exercise_log()
        dates = []
        pushup_counts = []
        squat_counts = []
        crunch_counts = []
        for date, data in exercise_log.items():
            dates.append(datetime.datetime.strptime(date, '%Y-%m-%d'))
            pushup_counts.append(data['pushups'])
            squat_counts.append(data['squats'])
            crunch_counts.append(data['crunches'])
        df = pd.DataFrame({
            'Date': dates,
            'Pushups': pushup_counts,
            'Squats': squat_counts,
            'Crunches': crunch_counts
        })
        st.line_chart(df.set_index('Date'))

if __name__ == "__main__":
    main()
