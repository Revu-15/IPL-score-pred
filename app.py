import streamlit as st
import pandas as pd
import pickle

# Load model and encoders
model = pickle.load(open('model.pkl', 'rb'))
encoders = pickle.load(open('encoder.pkl', 'rb'))

bat_team_enc, bowl_team_enc, venue_enc = encoders

st.title("🏏 IPL Score Prediction App")

# Team and venue options
teams = bat_team_enc.classes_
venues = venue_enc.classes_

# UI for user inputs
bat_team = st.selectbox("Batting Team", teams)
bowl_team = st.selectbox("Bowling Team", teams)
venue = st.selectbox("Venue", venues)

overs = st.slider("Overs Completed", 5.0, 20.0, 10.0, 0.1)
runs = st.number_input("Current Runs", min_value=0, value=75)
wickets = st.number_input("Wickets Fallen", min_value=0, max_value=10, value=2)
run_rate = runs / overs if overs else 0

if st.button("Predict Final Score"):
    # Encode categorical inputs
    bat_team_enc_val = bat_team_enc.transform([bat_team])[0]
    bowl_team_enc_val = bowl_team_enc.transform([bowl_team])[0]
    venue_enc_val = venue_enc.transform([venue])[0]

    # Create input DataFrame
    input_df = pd.DataFrame([[bat_team_enc_val, bowl_team_enc_val, venue_enc_val, overs, runs, wickets, run_rate]],
                            columns=['bat_team', 'bowl_team', 'venue', 'overs', 'runs', 'wickets', 'run_rate'])

    prediction = model.predict(input_df)[0]
    st.success(f"🏆 Predicted Final Score: {int(prediction)} runs")
