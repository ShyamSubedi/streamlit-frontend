
import streamlit as st
import requests
import pandas as pd
from supabase import create_client

# Supabase setup
SUPABASE_URL = "https://oehpyaughmlhynmuhzrk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9laHB5YXVnaG1saHlubXVoenJrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMwMTYxOTUsImV4cCI6MjA1ODU5MjE5NX0.CPMU5-sEy2krskO27pwXB_85XaX6vtC75WxjKhGr3gk"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# API endpoint
API_URL = "https://your-app-name.onrender.com/predict/"  # Replace with your actual API URL

# Streamlit UI
st.set_page_config(page_title="Fraud Detection", layout="centered")
st.title("🛡️ Fraud Detection App")
st.write("Enter a transaction amount to check if it's fraudulent.")

amount = st.number_input("💰 Transaction Amount", min_value=0.01, step=0.01)

if st.button("🔍 Predict"):
    with st.spinner("Sending to API..."):
        try:
            response = requests.post(API_URL, json={"amount": amount})
            result = response.json()
            st.success("✅ Prediction received!")
            st.metric("Fraud Prediction", result["fraud_prediction"])
            st.metric("Fraud Probability", round(result["fraud_probability"], 6))
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.subheader("📊 Past Predictions (from Supabase)")

try:
    data = supabase.table("new_logs").select("*").order("timestamp", desc=True).limit(10).execute()
    df = pd.DataFrame(data.data)
    st.dataframe(df)
except Exception as e:
    st.warning(f"Could not fetch logs: {e}")
